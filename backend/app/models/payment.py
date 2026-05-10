from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.configs.database import Base


class ThanhToan(Base):
    __tablename__ = "thanh_toan"

    id = Column(Integer, primary_key=True, index=True)
    id_don_hang = Column(Integer, ForeignKey("don_hang.id", ondelete="CASCADE"), unique=True, nullable=False)
    phuong_thuc = Column(String(50), nullable=False)
    so_tien = Column(Float, nullable=False)
    trang_thai = Column(String(30), default="cho_xu_ly")
    ma_giao_dich = Column(String(255), nullable=True)
    thoi_diem_thanh_toan = Column(DateTime(timezone=True), nullable=True)
    ngay_tao = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    don_hang = relationship("DonHang", back_populates="thanh_toan")
