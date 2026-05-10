# 👟 Giày Đẹp Store - Hệ Thống Quản Lý Hiện Đại

Chào mừng bạn đến với dự án **Giày Đẹp Store**, một nền tảng thương mại điện tử chuyên biệt cho giày dép với giao diện cao cấp và công nghệ hiện đại.

## 📂 Tài liệu chi tiết

Để hiểu rõ hơn về dự án, vui lòng tham khảo các tài liệu trong thư mục `agent/`:

-   [✨ Chức năng hệ thống](agent/FEATURES.md): Danh sách đầy đủ tính năng Client & Admin.
-   [🛠️ Công nghệ & Kiến trúc](agent/TECH_STACK.md): Chi tiết về bộ công cụ và cách tổ chức dự án.
-   [⚠️ Xử lý lỗi](agent/EXCEPTIONS.md): Quy ước về mã lỗi và ngoại lệ.
-   [📋 Tiến độ dự án](agent/CHECKLIST.md): Trạng thái hoàn thiện của các đầu việc.

## 🚀 Hướng dẫn khởi chạy nhanh

### ⚙️ Backend (Python FastAPI)
```bash
cd backend
python -m venv venv
# Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

### 🎨 Frontend (Vue.js 3)
```bash
cd frontend
npm install
npm run dev
```

## 👤 Tài khoản mặc định (Sau khi khởi tạo)
- **Quản trị viên:** `admin@qlbg.com` / `admin123`
- **Khách hàng mẫu:** Có thể tạo trực tiếp qua giao diện Đăng ký.

---
*Dự án được phát triển với tiêu chuẩn kỹ thuật cao, sẵn sàng cho việc mở rộng và vận hành thực tế.*
