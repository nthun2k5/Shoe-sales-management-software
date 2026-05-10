from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PhanHoiThanhToan(BaseModel):
    id: int
    id_don_hang: int
    phuong_thuc: str
    so_tien: float
    trang_thai: str
    ma_giao_dich: Optional[str] = None
    thoi_diem_thanh_toan: Optional[datetime] = None
    ngay_tao: Optional[datetime] = None

    class Config:
        from_attributes = True


class XacNhanThanhToan(BaseModel):
    ma_giao_dich: Optional[str] = None
