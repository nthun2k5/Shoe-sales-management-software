from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.configs.database import Base


class NhatKy(Base):
    __tablename__ = "nhat_ky"

    id = Column(Integer, primary_key=True, index=True)
    nguoi_dung_id = Column(Integer, ForeignKey("nguoi_dung.id"), nullable=True)
    hanh_dong = Column(String(100), nullable=False)  # e.g., "CREATE", "UPDATE", "DELETE", "LOGIN"
    mo_ta = Column(Text, nullable=True)
    ip_address = Column(String(45), nullable=True)  # IPv4 or IPv6
    id_don_hang = Column(Integer, nullable=True) # Reference to order ID
    ngay_tao = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    nguoi_dung = relationship("NguoiDung")
