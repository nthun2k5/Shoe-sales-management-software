from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.configs.database import Base


class ThongTinNganHang(Base):
    __tablename__ = "thong_tin_ngan_hang"

    id = Column(Integer, primary_key=True, index=True)
    loai = Column(String(20), nullable=False, default="ngan_hang")  # "ngan_hang" or "vi_dien_tu"
    ten_ngan_hang = Column(String(100), nullable=False)  # Tên ngân hàng hoặc ví
    ma_ngan_hang = Column(String(20), nullable=True)  # Mã ngân hàng (VCB, TCB...) - chỉ cho ngân hàng
    chu_tai_khoan = Column(String(100), nullable=True)  # Chủ tài khoản - chỉ cho ngân hàng
    so_tai_khoan = Column(String(50), nullable=True)  # STK - chỉ cho ngân hàng
    so_dien_thoai = Column(String(20), nullable=True)  # SĐT nhận tiền - cho ví điện tử
    chi_nhanh = Column(String(100), nullable=True)
    dang_su_dung = Column(Boolean, default=True)
    ngay_tao = Column(DateTime(timezone=True), server_default=func.now())
    ngay_cap_nhat = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
