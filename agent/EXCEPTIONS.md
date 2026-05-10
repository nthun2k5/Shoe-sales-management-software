# ⚠️ Xử lý lỗi & Ngoại lệ - Giày Đẹp Store

Dự án áp dụng quy trình xử lý lỗi tập trung để đảm bảo tính ổn định và cung cấp phản hồi rõ ràng cho người dùng.

## 🌐 1. Backend (API Exceptions)

Hệ thống sử dụng các mã lỗi HTTP tiêu chuẩn kết hợp với thông báo chi tiết:

- **400 Bad Request**: Dữ liệu đầu vào không hợp lệ (lỗi validation Pydantic).
- **401 Unauthorized**: Token hết hạn hoặc không hợp lệ.
- **403 Forbidden**: Người dùng không có quyền truy cập (ví dụ: khách truy cập trang Admin).
- **404 Not Found**: Không tìm thấy tài nguyên (Sản phẩm, Đơn hàng...).
- **409 Conflict**: Dữ liệu đã tồn tại (ví dụ: Email đã được đăng ký).
- **422 Unprocessable Entity**: Lỗi logic nghiệp vụ hoặc cấu trúc dữ liệu không khớp.
- **500 Internal Server Error**: Lỗi hệ thống không xác định (được log lại để kiểm tra).

**Cấu trúc phản hồi lỗi:**
```json
{
  "detail": "Thông báo lỗi chi tiết dành cho người dùng"
}
```

## 🎨 2. Frontend (UI Error Handling)

Frontend xử lý lỗi thông qua `Interceptor` của Axios và `Composable`:

- **Global Toast**: Sử dụng `useToast` để hiển thị thông báo lỗi/thành công ở góc màn hình.
- **Form Validation**: Kiểm tra dữ liệu ngay tại giao diện trước khi gửi đi.
- **Loading State**: Hiển thị Skeleton hoặc Spinner khi dữ liệu đang tải để tránh lỗi tương tác.
- **Image Fallback**: Tự động hiển thị ảnh mặc định nếu ảnh sản phẩm bị lỗi hoặc không tồn tại.
- **Route Guards**: Ngăn chặn truy cập trái phép vào các trang bảo mật/Admin ngay từ phía Client.

## 🛠️ 3. Quy trình gỡ lỗi (Debugging)

- **Backend Logs**: Các lỗi nghiêm trọng được ghi lại trong bảng `logs` của database và hiển thị tại trang Admin Logs.
- **Frontend Console**: Sử dụng log có cấu trúc để theo dõi luồng dữ liệu trong quá trình phát triển.
- **Database Migrations**: Sử dụng Alembic để xử lý lỗi khi thay đổi cấu trúc dữ liệu mà không làm mất data hiện có.
