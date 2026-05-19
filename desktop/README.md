# 🖥️ GIÀY ĐẸP STORE - DESKTOP APPLICATION

Ứng dụng Desktop chính thức của hệ thống **Quản lý Bán hàng Giày Đẹp Store**, được xây dựng trên nền tảng **Electron** mạnh mẽ. Ứng dụng đóng vai trò là một lớp vỏ (Wrapper) chuyên nghiệp, kết nối trực tiếp đến hệ thống Web App, mang lại trải nghiệm mượt mà, độc lập và tiện lợi như một phần mềm Native trên Windows.

---

## 🌟 TÍNH NĂNG NỔI BẬT

- **Giao diện Tràn viền (Borderless / Clean UI):** Tự động ẩn thanh menu rườm rà của trình duyệt, tối ưu hóa không gian làm việc cho nhân viên bán hàng và quản lý.
- **Tự động Kết nối & Chuyển đổi Thông minh:** Tự động kết nối đến hệ thống máy chủ web (`http://localhost:5173`).
- **Màn hình Chờ / Fallback Hiện đại:** Nếu máy chủ web chưa khởi động hoặc mất kết nối, ứng dụng hiển thị màn hình Fallback Glassmorphism tuyệt đẹp kèm hướng dẫn chi tiết và cơ chế tự động thử lại (Auto-retry) mỗi 5 giây.
- **Tích hợp Sẵn Cơ chế Đóng gói (.exe):** Cấu hình chuẩn xác với `electron-builder`, cho phép xuất file cài đặt chỉ với một câu lệnh.

---

## 🚀 HƯỚNG DẪN SỬ DỤNG VÀ CHẠY ỨNG DỤNG

### Bước 1: Khởi động máy chủ Web App (Frontend & Backend)
Để ứng dụng Desktop có thể tải đầy đủ dữ liệu, bạn cần chắc chắn rằng Frontend (Vite) đang chạy:
1. Mở Terminal / Command Prompt tại thư mục gốc của dự án.
2. Di chuyển vào thư mục frontend:
   ```bash
   cd frontend
   ```
3. Khởi động máy chủ Vite:
   ```bash
   npm run dev
   ```
*(Máy chủ sẽ chạy tại địa chỉ `http://localhost:5173`)*

---

### Bước 2: Khởi động Ứng dụng Desktop
1. Mở một cửa sổ Terminal / Command Prompt mới.
2. Di chuyển vào thư mục `desktop`:
   ```bash
   cd desktop
   ```
3. Khởi chạy ứng dụng Electron:
   ```bash
   npm start
   ```

---

## 📦 HƯỚNG DẪN ĐÓNG GÓI THÀNH FILE CÀI ĐẶT (`.exe`)

Bạn có thể dễ dàng đóng gói ứng dụng thành file thực thi độc lập để cài đặt trên các máy tính khác (máy POS tại cửa hàng, máy tính của nhân viên, v.v.):

1. Mở Terminal tại thư mục `desktop`.
2. Chạy lệnh đóng gói:
   ```bash
   npm run dist
   ```
3. Sau khi quá trình hoàn tất, file cài đặt `.exe` sẽ xuất hiện trong thư mục `desktop/dist/`.

---

## 📁 CẤU TRÚC THƯ MỤC `desktop/`

```text
desktop/
│
├── assets/
│   └── icon.png          # Biểu tượng (Icon) chính thức của ứng dụng
│
├── dist/                 # Thư mục chứa file .exe sau khi đóng gói (tự động tạo)
│
├── fallback.html         # Màn hình chờ kết nối / hướng dẫn khởi động server
├── main.js               # Tiến trình chính (Main Process) quản lý vòng đời Electron
├── package.json          # Cấu hình thư viện và kịch bản đóng gói electron-builder
└── README.md             # Tài liệu hướng dẫn sử dụng ứng dụng Desktop
```
