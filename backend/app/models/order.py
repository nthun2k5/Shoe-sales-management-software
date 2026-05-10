from sqlalchemy import Column, Integer, String, DateTime, Text, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.configs.database import Base


class DonHang(Base):
    __tablename__ = "don_hang"

    id = Column(Integer, primary_key=True, index=True)
    id_nguoi_dung = Column(Integer, ForeignKey("nguoi_dung.id"), nullable=False)
    ma_don_hang = Column(String(50), unique=True, index=True, nullable=False)
    tong_tien = Column(Float, default=0)
    tien_giam_gia = Column(Float, default=0)
    phi_van_chuyen = Column(Float, default=0)
    thanh_tien = Column(Float, default=0)
    trang_thai = Column(String(30), default="cho_xu_ly")
    phuong_thuc_thanh_toan = Column(String(50), nullable=True)
    trang_thai_thanh_toan = Column(String(30), default="chua_thanh_toan")
    ten_nguoi_nhan = Column(String(255), nullable=True)
    sdt_nguoi_nhan = Column(String(20), nullable=True)
    dia_chi_nhan = Column(Text, nullable=True)
    ghi_chu = Column(Text, nullable=True)
    ngay_tao = Column(DateTime(timezone=True), server_default=func.now())
    ngay_cap_nhat = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    nguoi_dung = relationship("NguoiDung", back_populates="don_hangs")
    chi_tiet_don_hangs = relationship("ChiTietDonHang", back_populates="don_hang", cascade="all, delete-orphan")
    thanh_toan = relationship("ThanhToan", back_populates="don_hang", uselist=False)


class ChiTietDonHang(Base):
    __tablename__ = "chi_tiet_don_hang"

    id = Column(Integer, primary_key=True, index=True)
    id_don_hang = Column(Integer, ForeignKey("don_hang.id", ondelete="CASCADE"), nullable=False)
    id_san_pham = Column(Integer, ForeignKey("san_pham.id"), nullable=False)
    kich_thuoc = Column(String(50), nullable=True)
    so_luong = Column(Integer, nullable=False)
    don_gia = Column(Float, nullable=False)
    thanh_tien = Column(Float, nullable=False)

    # Relationships
    don_hang = relationship("DonHang", back_populates="chi_tiet_don_hangs")
    san_pham = relationship("SanPham", back_populates="chi_tiet_don_hangs")
