from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class NhatKyBase(BaseModel):
    hanh_dong: str
    mo_ta: Optional[str] = None
    ip_address: Optional[str] = None
    id_don_hang: Optional[int] = None


class NhatKyCreate(NhatKyBase):
    nguoi_dung_id: Optional[int] = None


class NhatKy(NhatKyBase):
    id: int
    nguoi_dung_id: Optional[int] = None
    ten_nguoi_dung: Optional[str] = None
    ngay_tao: datetime

    class Config:
        from_attributes = True
