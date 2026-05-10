from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.configs.database import Base


class NguoiDung(Base):
    __tablename__ = "nguoi_dung"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    mat_khau_hash = Column(String(255), nullable=False)
    ho_ten = Column(String(255), nullable=False)
    so_dien_thoai = Column(String(20), nullable=True)
    dia_chi = Column(Text, nullable=True)
    vai_tro = Column(String(20), default="khach", nullable=False)
    anh_dai_dien = Column(Text, nullable=True)
    dang_hoat_dong = Column(Boolean, default=True)
    ngay_tao = Column(DateTime(timezone=True), server_default=func.now())
    ngay_cap_nhat = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    don_hangs = relationship("DonHang", back_populates="nguoi_dung")
    gio_hangs = relationship("GioHang", back_populates="nguoi_dung", cascade="all, delete-orphan")
    danh_sach_yeu_thichs = relationship("DanhSachYeuThich", back_populates="nguoi_dung", cascade="all, delete-orphan")
    danh_gias = relationship("DanhGia", back_populates="nguoi_dung")
    dia_chi_giao_hangs = relationship("DiaChiGiaoHang", back_populates="nguoi_dung", cascade="all, delete-orphan")
