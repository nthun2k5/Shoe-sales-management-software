from sqlalchemy import Column, Integer, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.configs.database import Base


class DanhSachYeuThich(Base):
    __tablename__ = "danh_sach_yeu_thich"

    id = Column(Integer, primary_key=True, index=True)
    id_nguoi_dung = Column(Integer, ForeignKey("nguoi_dung.id", ondelete="CASCADE"), nullable=False)
    id_san_pham = Column(Integer, ForeignKey("san_pham.id", ondelete="CASCADE"), nullable=False)
    ngay_tao = Column(DateTime(timezone=True), server_default=func.now())

    # Ensure unique user-product pairs
    __table_args__ = (UniqueConstraint("id_nguoi_dung", "id_san_pham", name="uq_nguoi_dung_san_pham_yeu_thich"),)

    # Relationships
    nguoi_dung = relationship("NguoiDung", back_populates="danh_sach_yeu_thichs")
    san_pham = relationship("SanPham", back_populates="danh_sach_yeu_thichs")
