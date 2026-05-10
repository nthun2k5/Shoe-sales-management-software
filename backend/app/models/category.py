from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.configs.database import Base


class DanhMuc(Base):
    __tablename__ = "danh_muc"

    id = Column(Integer, primary_key=True, index=True)
    ten = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, index=True, nullable=False)
    mo_ta = Column(Text, nullable=True)
    anh = Column(Text, nullable=True)
    id_cha = Column(Integer, ForeignKey("danh_muc.id"), nullable=True)
    dang_hoat_dong = Column(Boolean, default=True)
    ngay_tao = Column(DateTime(timezone=True), server_default=func.now())
    ngay_cap_nhat = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    cha = relationship("DanhMuc", remote_side=[id], backref="con_cais")
    san_phams = relationship("SanPham", back_populates="danh_muc")
