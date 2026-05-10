# 🎨 Giày Đẹp Store - Frontend

Ứng dụng Client và Admin Dashboard được xây dựng bằng **Vue.js 3** và **Tailwind CSS v4**.

## 🚀 Tính năng chính

- **Trang chủ hiện đại**: Slider động, Flash Sale Carousel, Danh mục nổi bật.
- **Mua sắm thông minh**: Bộ lọc sản phẩm, Tìm kiếm thời gian thực, Giỏ hàng & Yêu thích.
- **Admin Dashboard**: Quản lý toàn diện Sản phẩm, Đơn hàng, Người dùng và Thống kê trực quan.
- **Hiệu ứng mượt mà**: Tích hợp AOS (Animate on Scroll) và các micro-interactions cao cấp.

## 🛠 Công nghệ

- **Framework**: Vue 3 (Script Setup)
- **Styling**: Tailwind CSS v4 + Custom Modern CSS
- **State**: Pinia (Auth, Cart, Wishlist)
- **Routing**: Vue Router 4
- **Animations**: AOS, Tailwind Transitions

## ⚡ Khởi chạy

```bash
# Cài đặt dependencies
npm install

# Chạy ở chế độ phát triển
npm run dev

# Xây dựng bản production
npm run build
```

## 📁 Cấu trúc src/

- `assets/`: Hình ảnh, font chữ và styles toàn cục.
- `components/`: Các thành phần UI tái sử dụng.
- `layouts/`: Khung giao diện (ClientLayout, AdminLayout).
- `stores/`: Quản lý trạng thái Pinia.
- `views/`: Các trang giao diện chính.
- `services/`: Cấu hình API Axios.
