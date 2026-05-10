from pydantic import BaseModel
from typing import Optional


class DiaChiBase(BaseModel):
    ten_nguoi_nhan: str
    so_dien_thoai: str
    dia_chi: str
    la_mac_dinh: bool = False


class DiaChiTao(DiaChiBase):
    pass


class DiaChiCapNhat(BaseModel):
    ten_nguoi_nhan: Optional[str] = None
    so_dien_thoai: Optional[str] = None
    dia_chi: Optional[str] = None
    la_mac_dinh: Optional[bool] = None


class DiaChiPhanHoi(DiaChiBase):
    id: int
    id_nguoi_dung: int

    class Config:
        from_attributes = True
