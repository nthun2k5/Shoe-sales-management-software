# ⚙️ Giày Đẹp Store - Backend API

Hệ thống API mạnh mẽ được xây dựng bằng **FastAPI** và **PostgreSQL**.

## 🚀 Công nghệ sử dụng

- **FastAPI**: Framework web Python hiện đại, hiệu năng cao.
- **SQLAlchemy**: ORM mạnh mẽ để tương tác với Database.
- **PostgreSQL**: Cơ sở dữ liệu quan hệ tin cậy.
- **JWT**: Bảo mật tài khoản qua Access & Refresh Token.
- **Uvicorn**: Máy chủ ASGI tốc độ cao.

## ⚡ Cài đặt

1. Tạo môi trường ảo:
```bash
python -m venv venv
source venv/bin/activate # Windows: venv\Scripts\activate
```

2. Cài đặt thư viện:
```bash
pip install -r requirements.txt
```

3. Cấu hình file `.env`:
Tạo file `.env` và điền thông tin kết nối DB.

4. Khởi chạy:
```bash
python -m uvicorn app.main:app --reload
```

## 📚 API Documentation

Sau khi chạy server, bạn có thể truy cập tài liệu API tự động tại:
- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

## 📁 Cấu trúc app/

- `models/`: Định nghĩa các bảng Database.
- `routers/`: Xử lý các endpoint API.
- `schemas/`: Định nghĩa kiểu dữ liệu (Pydantic).
- `utils/`: Các hàm tiện ích (Bảo mật, Logic chung).
- `configs/`: Cấu hình hệ thống và Database.
