from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.configs.database import Base


class DiaChiGiaoHang(Base):
    __tablename__ = "dia_chi_giao_hang"

    id = Column(Integer, primary_key=True, index=True)
    id_nguoi_dung = Column(Integer, ForeignKey("nguoi_dung.id", ondelete="CASCADE"), nullable=False)
    ten_nguoi_nhan = Column(String(255), nullable=False)
    so_dien_thoai = Column(String(20), nullable=False)
    dia_chi = Column(Text, nullable=False)
    la_mac_dinh = Column(Boolean, default=False)

    # Relationships
    nguoi_dung = relationship("NguoiDung", back_populates="dia_chi_giao_hangs")
