from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.configs.database import Base


class GioHang(Base):
    __tablename__ = "gio_hang"

    id = Column(Integer, primary_key=True, index=True)
    id_nguoi_dung = Column(Integer, ForeignKey("nguoi_dung.id", ondelete="CASCADE"), nullable=False)
    id_san_pham = Column(Integer, ForeignKey("san_pham.id", ondelete="CASCADE"), nullable=False)
    kich_thuoc = Column(String(50), nullable=True)
    so_luong = Column(Integer, default=1)
    ngay_tao = Column(DateTime(timezone=True), server_default=func.now())
    ngay_cap_nhat = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    nguoi_dung = relationship("NguoiDung", back_populates="gio_hangs")
    san_pham = relationship("SanPham", back_populates="gio_hangs")
