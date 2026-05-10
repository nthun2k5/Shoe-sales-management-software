from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.sql import func
from app.configs.database import Base


class PhuongThucThanhToan(Base):
    __tablename__ = "phuong_thuc_thanh_toan"

    id = Column(Integer, primary_key=True, index=True)
    ma_phuong_thuc = Column(String(50), unique=True, index=True, nullable=False)
    ten_phuong_thuc = Column(String(100), nullable=False)
    mo_ta = Column(String(255), nullable=True)
    icon_svg = Column(String(1000), nullable=True)
    anh_logo = Column(String(255), nullable=True, comment="URL ảnh logo")
    kich_hoat = Column(Boolean, default=True)
    ho_tro_qr = Column(Boolean, default=False, comment="Hỗ trợ thanh toán QR")

    # Phân loại & Thứ tự
    loai = Column(String(50), default="other", comment="Loại: cod, bank, momo, zalopay, other")
    thu_tu = Column(Integer, default=0, comment="Thứ tự ưu tiên hiển thị")

    # Phí thanh toán
    phi_co_dinh = Column(Integer, default=0, comment="Phí cố định (VND)")
    phi_phan_tram = Column(Integer, default=0, comment="Phí phần trăm (%)")

    # Quy tắc đơn hàng
    gia_tri_don_toi_thieu = Column(Integer, nullable=True, comment="Giá trị đơn tối thiểu (VND)")
    gia_tri_don_toi_da = Column(Integer, nullable=True, comment="Giá trị đơn tối đa (VND)")

    # Cấu hình API
    cau_hinh_json = Column(Text, nullable=True, comment="Cấu hình API (JSON)")

    ngay_tao = Column(DateTime(timezone=True), server_default=func.now())
    ngay_cap_nhat = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
