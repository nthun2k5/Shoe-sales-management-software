from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.configs.database import Base


class MaGiamGia(Base):
    __tablename__ = "ma_giam_gia"

    id = Column(Integer, primary_key=True, index=True)
    ma = Column(String(50), unique=True, index=True, nullable=False)
    loai_giam_gia = Column(String(20), nullable=False)
    gia_tri_giam = Column(Float, nullable=False)
    gia_tri_don_toi_thieu = Column(Float, default=0)
    so_lan_su_dung_toi_da = Column(Integer, default=0)
    so_lan_da_su_dung = Column(Integer, default=0)
    ngay_bat_dau = Column(DateTime(timezone=True), nullable=True)
    ngay_ket_thuc = Column(DateTime(timezone=True), nullable=True)
    dang_hoat_dong = Column(Boolean, default=True)
    ngay_tao = Column(DateTime(timezone=True), server_default=func.now())

    su_dung = relationship("SuDungMaGiamGia", back_populates="ma_giam_gia", cascade="all, delete-orphan")


class SuDungMaGiamGia(Base):
    __tablename__ = "su_dung_ma_giam_gia"

    id = Column(Integer, primary_key=True, index=True)
    id_nguoi_dung = Column(Integer, ForeignKey("nguoi_dung.id"), nullable=False)
    id_ma_giam_gia = Column(Integer, ForeignKey("ma_giam_gia.id"), nullable=False)
    ngay_su_dung = Column(DateTime(timezone=True), server_default=func.now())

    nguoi_dung = relationship("NguoiDung")
    ma_giam_gia = relationship("MaGiamGia", back_populates="su_dung")
