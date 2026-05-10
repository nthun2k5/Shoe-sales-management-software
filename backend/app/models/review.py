from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.configs.database import Base


class DanhGia(Base):
    __tablename__ = "danh_gia"

    id = Column(Integer, primary_key=True, index=True)
    id_nguoi_dung = Column(Integer, ForeignKey("nguoi_dung.id"), nullable=False)
    id_san_pham = Column(Integer, ForeignKey("san_pham.id", ondelete="CASCADE"), nullable=False)
    diem_danh_gia = Column(Integer, nullable=False)
    binh_luan = Column(Text, nullable=True)
    ngay_tao = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    nguoi_dung = relationship("NguoiDung", back_populates="danh_gias")
    san_pham = relationship("SanPham", back_populates="danh_gias")
