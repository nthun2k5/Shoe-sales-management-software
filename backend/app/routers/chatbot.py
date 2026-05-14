from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import text
import google.generativeai as genai # Vẫn giữ để tránh lỗi import ở main nếu cần, nhưng sẽ dùng SDK mới bên dưới
from google import genai as new_genai
from google.genai import errors
import re

from app.configs.database import get_db
from app.configs.config import settings

router = APIRouter(prefix="/api/chatbot", tags=["Chatbot"])

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

def get_client():
    if not settings.GEMINI_API_KEY or settings.GEMINI_API_KEY == "your_gemini_api_key_here":
        raise HTTPException(status_code=500, detail="Chưa cấu hình GEMINI_API_KEY")
    return new_genai.Client(api_key=settings.GEMINI_API_KEY)

SCHEMA_PROMPT = """
You are a STRICTOR Shoe Consultant AI.
Analyze the user's message:
1. If greeting/small talk: return 'GENERAL_TALK'.
2. If shoe search/consultation: translate to a SELECT query.
3. If unrelated to shoes/shop: return 'REJECTED_REQUEST'.

Tables:
- san_pham (id, ten, gia, thuong_hieu, mo_ta_ngan)
- danh_muc (id, ten)

Rules:
- DB content is UNACCENTED Vietnamese (e.g. 'Giay').
- Remove accents from search terms.
- Use ILIKE with % wildcards (e.g. %giay%oxford%).
- Return ONLY raw SQL. No markdown.

User: {user_message}
"""

def is_safe_sql(sql: str) -> bool:
    if sql in ["GENERAL_TALK", "REJECTED_REQUEST"]:
        return True
    sql_lower = sql.lower().strip()
    if not sql_lower.startswith("select"):
        return False
    forbidden = ["insert", "update", "delete", "drop", "truncate", "nguoi_dungs", "don_hangs"]
    for kw in forbidden:
        if re.search(r'\b' + kw + r'\b', sql_lower):
            return False
    return True

@router.post("/ask", response_model=ChatResponse)
def ask_chatbot(request: ChatRequest, db: Session = Depends(get_db)):
    try:
        client = get_client()
    except Exception:
        return ChatResponse(reply="Hệ thống AI đang bảo trì.")

    user_msg = request.message
    
    # Bước 1: Sinh SQL
    try:
        res1 = client.models.generate_content(
            model='gemini-flash-latest', 
            contents=SCHEMA_PROMPT.format(user_message=user_msg)
        )
        sql_query = res1.text.strip().replace("```sql", "").replace("```", "").strip()
    except errors.ClientError as e:
        if "429" in str(e):
            return ChatResponse(reply="Bạn đã hết lượt hỏi miễn phí trong ngày. Vui lòng thử lại sau ít phút!")
        return ChatResponse(reply="Tôi không thể xử lý yêu cầu này lúc này.")
    except Exception:
        return ChatResponse(reply="Tôi không thể phân tích câu hỏi của bạn.")

    if not is_safe_sql(sql_query):
        return ChatResponse(reply="Yêu cầu không hợp lệ.")

    result_data = []
    if sql_query == "REJECTED_REQUEST":
        p2 = f"Từ chối tư vấn vì không phải về giày. Câu hỏi: {user_msg}"
    elif sql_query == "GENERAL_TALK":
        result_data = None
        p2 = f"Chào lại khách hàng thân thiện. Câu hỏi: {user_msg}"
    else:
        try:
            result = db.execute(text(sql_query)).mappings().all()
            result_data = [dict(row) for row in result]
            p2 = f"Tư vấn giày dựa trên dữ liệu: {result_data}. Câu hỏi: {user_msg}. Trả lời ngắn gọn, chuyên nghiệp bằng tiếng Việt."
        except Exception:
            result_data = []
            p2 = f"Xin lỗi vì không tìm thấy sản phẩm. Câu hỏi: {user_msg}"

    try:
        res2 = client.models.generate_content(model='gemini-flash-latest', contents=p2)
        return ChatResponse(reply=res2.text.strip())
    except errors.ClientError as e:
        if "429" in str(e):
            return ChatResponse(reply="Bạn đã hết lượt hỏi miễn phí trong ngày. Vui lòng thử lại sau ít phút!")
        return ChatResponse(reply="Hệ thống đang bận.")
    except Exception:
        return ChatResponse(reply="Hệ thống đang bận.")
