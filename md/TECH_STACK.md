# 🛠️ Công nghệ & Kiến trúc - Giày Đẹp Store

Dự án sử dụng bộ công cụ hiện đại (Modern Full-stack) nhằm đảm bảo hiệu năng cao, trải nghiệm người dùng mượt mà và khả năng bảo trì dễ dàng.

## 🎨 Frontend (Giao diện người dùng)

-   **Framework:** [Vue.js 3](https://vuejs.org/) (Composition API) - Hiệu năng cao, phản hồi nhanh.
-   **Build Tool:** [Vite](https://vitejs.dev/) - Tốc độ phát triển và đóng gói cực nhanh.
-   **State Management:** [Pinia](https://pinia.vuejs.org/) - Quản lý trạng thái tập trung (Auth, Giỏ hàng, Wishlist).
-   **Styling:** [Tailwind CSS v4](https://tailwindcss.com/) - Hệ thống CSS utility-first mới nhất cho thiết kế hiện đại.
-   **Routing:** [Vue Router 4](https://router.vuejs.org/) - Điều hướng trang mượt mà.
-   **Animation:** [AOS (Animate On Scroll)](https://michalsnik.github.io/aos/) - Hiệu ứng chuyển động khi cuộn trang.
-   **Charts:** [Chart.js](https://www.chartjs.org/) & [vue-chartjs](https://vue-chartjs.org/) - Biểu đồ thống kê trực quan cho Admin.
-   **Data Export:** [XLSX](https://github.com/SheetJS/sheetjs) - Xuất dữ liệu đơn hàng/sản phẩm ra file Excel.
-   **HTTP Client:** [Axios](https://axios-http.com/) - Giao tiếp với API Backend.

## ⚙️ Backend (Hệ thống xử lý)

-   **Framework:** [FastAPI](https://fastapi.tiangolo.com/) - Python framework hiện đại, hiệu năng cực cao (ngang ngửa Go/Node.js).
-   **ORM:** [SQLAlchemy](https://www.sqlalchemy.org/) - Ánh xạ dữ liệu Python sang SQL một cách linh hoạt.
-   **Database:** [PostgreSQL](https://www.postgresql.org/) - Hệ quản trị cơ sở dữ liệu quan hệ mạnh mẽ, tin cậy.
-   **Authentication:** [JWT (JSON Web Tokens)](https://jwt.io/) - Xác thực người dùng dựa trên token an toàn.
-   **Password Hashing:** [Bcrypt](https://pypi.org/project/bcrypt/) - Mã hóa mật khẩu an toàn theo tiêu chuẩn ngành.
-   **Validation:** [Pydantic v2](https://docs.pydantic.dev/) - Xác thực dữ liệu đầu vào và định dạng phản hồi API.
-   **Migrations:** [Aembic](https://alembic.sqlalchemy.org/) - Quản lý lịch sử thay đổi cấu trúc database.

## 📐 Kiến trúc hệ thống

1.  **Decoupled Architecture:** Frontend và Backend hoàn toàn tách biệt, giao tiếp qua RESTful API.
2.  **Service Layer:** Logic nghiệp vụ được xử lý tập trung giúp code Backend sạch sẽ và dễ kiểm thử.
3.  **Premium UI Design:** Áp dụng phong cách **Glassmorphism** và **Minimalist Luxury** với bo góc lớn, bóng đổ tầng và làm mờ nền.
4.  **Security First:** 
    *   Mã hóa mật khẩu 2 lớp.
    *   Bảo vệ route bằng middleware xác thực.
    *   Ngăn chặn copy/chuột phải (tùy chọn) để bảo vệ bản quyền hình ảnh.
