# GEMINI.md - Ngữ cảnh Cửa hàng Giày Đẹp (Final)

Tài liệu này cung cấp các ngữ cảnh và hướng dẫn thiết yếu cho các AI agent làm việc trong dự án **Giày Đẹp Store**, một hệ thống quản lý cửa hàng giày hiện đại.

## 🚀 Tổng quan dự án

**Giày Đẹp Store** là một nền tảng thương mại điện tử full-stack đã hoàn thiện, với trọng tâm là UI/UX "Premium" (Minimalist Luxury, Glassmorphism) và hiệu suất cao.

## 📂 Tài liệu đóng gói
Để hỗ trợ việc bảo trì và nâng cấp, các tài liệu sau đã được tạo:
- `agent/FEATURES.md`: Danh sách chức năng đầy đủ.
- `agent/TECH_STACK.md`: Công nghệ và kiến trúc hệ thống.
- `agent/EXCEPTIONS.md`: Quy trình xử lý lỗi và ngoại lệ.
- `agent/CHECKLIST.md`: Trạng thái hoàn thành dự án (100%).

## 📂 Cấu trúc dự án

### Backend (`/backend`)
- `app/main.py`: Điểm nhập, đăng ký các router và khởi tạo dữ liệu mẫu.
- `app/models/`: Định nghĩa các thực thể PostgreSQL (SQLAlchemy).
- `app/routers/`: API endpoints tổ chức theo tính năng.
- `app/services/`: Lớp logic nghiệp vụ tập trung.

### Frontend (`/frontend`)
- `src/views/`: Giao diện trang (Admin, Client, Auth).
- `src/stores/`: Quản lý trạng thái bằng Pinia.
- `src/assets/`: Chứa `main.css` với các biến Tailwind v4.

## 🛠 Cài đặt và Chạy (Tóm tắt)
- **Backend:** Cài đặt `requirements.txt`, chạy `uvicorn app.main:app`.
- **Frontend:** Cài đặt `npm`, chạy `npm run dev`.

## 📝 Quy ước "Premium Design"
Dự án tuân thủ nghiêm ngặt các quy tắc thiết kế:
- **Typography:** Sử dụng `font-black` cho tiêu đề và `font-light/medium` cho nội dung.
- **Micro-interactions:** Mọi nút bấm và thẻ thông tin phải có hiệu ứng hover mượt mà.
- **Glassmorphism:** Sử dụng `backdrop-blur` cho các Modal và Drawer.
- **Minimalism:** Ưu tiên các đường gạch chân (underline) và khoảng trắng thay cho các viền thô cứng.

## 📦 Đóng gói & Backup
- Thư mục `/data`: Chứa thông tin hướng dẫn và script để đóng gói dự án.
