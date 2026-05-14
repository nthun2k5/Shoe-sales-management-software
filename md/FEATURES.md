# ✨ Danh sách Chức năng - Giày Đẹp Store

Dự án cung cấp một hệ thống quản lý bán hàng giày dép đầy đủ tính năng cho cả khách hàng và quản trị viên.

## 👤 1. Khách hàng (Client)

### 🔑 Tài khoản & Bảo mật
- **Đăng ký/Đăng nhập**: Hệ thống xác thực JWT.
- **Hồ sơ cá nhân**: Cập nhật thông tin, ảnh đại diện (initials), số điện thoại.
- **Bảo mật**: Thay đổi mật khẩu, quản lý trạng thái xác thực.
- **Địa chỉ**: Lưu trữ nhiều địa chỉ nhận hàng, thiết lập địa chỉ mặc định.

### 🛍️ Mua sắm
- **Danh sách sản phẩm**: Lọc theo danh mục, tìm kiếm theo tên, sắp xếp theo giá và ngày tạo.
- **Chi tiết sản phẩm**: Xem thông tin, chọn size, xem ảnh, đánh giá từ người mua khác.
- **Giỏ hàng**: Thêm/Xóa sản phẩm, cập nhật số lượng, drawer giỏ hàng thông minh.
- **Wishlist**: Lưu trữ danh sách sản phẩm yêu thích.

### 📦 Đơn hàng
- **Thanh toán**: Quy trình thanh toán tinh gọn, áp dụng mã giảm giá.
- **Lịch sử đơn hàng**: Tra cứu đơn hàng, lọc theo trạng thái (Chờ xử lý, Đang giao, Đã giao...).
- **Đánh giá**: Gửi đánh giá sao và bình luận sau khi nhận hàng thành công.
- **Hủy đơn**: Khách hàng có thể hủy đơn khi đang ở trạng thái chờ xử lý.

## 🛠️ 2. Quản trị viên (Admin)

### 📊 Tổng quan (Dashboard)
- **Thống kê doanh thu**: Biểu đồ tăng trưởng theo thời gian.
- **Tổng số**: Khách hàng, đơn hàng, sản phẩm, doanh thu tổng.
- **Đơn hàng gần đây**: Theo dõi nhanh các giao dịch mới nhất.

### 📦 Quản lý kho & Sản phẩm
- **Sản phẩm**: Thêm, sửa, xóa sản phẩm. Quản lý tồn kho chi tiết.
- **Hình ảnh**: Tải lên và quản lý ảnh sản phẩm (Base64).
- **Danh mục**: Quản lý nhóm sản phẩm.

### 📝 Quản lý vận hành
- **Đơn hàng**: Cập nhật trạng thái đơn hàng (Xác nhận -> Giao hàng -> Hoàn thành).
- **Người dùng**: Quản lý danh sách khách hàng, khóa/mở tài khoản.
- **Mã giảm giá**: Tạo và quản lý các chương trình khuyến mãi.
- **Nhật ký hệ thống**: Theo dõi các hoạt động quan trọng của Admin.

## 🌟 3. Tính năng UX Cao cấp
- **Top Announcement**: Thanh thông báo trượt tự động các chương trình ưu đãi.
- **AI Chatbot Consultant**: Trợ lý ảo thông minh tích hợp Gemini AI, hỗ trợ tư vấn sản phẩm, tìm kiếm thông minh và giải đáp thắc mắc 24/7.
- **Responsive Design**: Tương thích hoàn hảo trên Mobile, Tablet và Desktop.
- **Export Data**: Xuất báo cáo Excel chuyên nghiệp.
