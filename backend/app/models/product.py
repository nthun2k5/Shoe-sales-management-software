from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.configs.database import Base


class SanPham(Base):
    __tablename__ = "san_pham"

    id = Column(Integer, primary_key=True, index=True)
    ten = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, index=True, nullable=False)
    mo_ta = Column(Text, nullable=True)
    mo_ta_ngan = Column(String(500), nullable=True)
    gia = Column(Float, nullable=False)
    gia_khuyen_mai = Column(Float, nullable=True)
    so_luong_ton = Column(Integer, default=0)
    ma_sku = Column(String(100), unique=True, nullable=True)
    id_danh_muc = Column(Integer, ForeignKey("danh_muc.id"), nullable=True)
    thuong_hieu = Column(String(255), nullable=True)
    dang_hoat_dong = Column(Boolean, default=True)
    la_noi_bat = Column(Boolean, default=False)
    cac_kich_thuoc = Column(String(255), nullable=True)
    ngay_tao = Column(DateTime(timezone=True), server_default=func.now())
    ngay_cap_nhat = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    danh_muc = relationship("DanhMuc", back_populates="san_phams")
    anh_san_phams = relationship("AnhSanPham", back_populates="san_pham", cascade="all, delete-orphan")
    chi_tiet_don_hangs = relationship("ChiTietDonHang", back_populates="san_pham")
    gio_hangs = relationship("GioHang", back_populates="san_pham", cascade="all, delete-orphan")
    danh_sach_yeu_thichs = relationship("DanhSachYeuThich", back_populates="san_pham", cascade="all, delete-orphan")
    danh_gias = relationship("DanhGia", back_populates="san_pham", cascade="all, delete-orphan")


class AnhSanPham(Base):
    __tablename__ = "anh_san_pham"

    id = Column(Integer, primary_key=True, index=True)
    id_san_pham = Column(Integer, ForeignKey("san_pham.id", ondelete="CASCADE"), nullable=False)
    du_lieu_anh = Column(Text, nullable=False)
    la_anh_chinh = Column(Boolean, default=False)
    thu_tu_sap_xep = Column(Integer, default=0)

    # Relationships
    san_pham = relationship("SanPham", back_populates="anh_san_phams")
