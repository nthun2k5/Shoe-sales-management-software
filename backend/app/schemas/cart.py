from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class GioHangThem(BaseModel):
    id_san_pham: int
    kich_thuoc: Optional[str] = None
    so_luong: int = 1


class GioHangCapNhat(BaseModel):
    so_luong: int


class PhanHoiGioHangItem(BaseModel):
    id: int
    id_san_pham: int
    ten_san_pham: Optional[str] = None
    anh_san_pham: Optional[str] = None
    kich_thuoc: Optional[str] = None
    gia_san_pham: Optional[float] = None
    gia_khuyen_mai: Optional[float] = None
    so_luong: int
    thanh_tien: Optional[float] = None

    class Config:
        from_attributes = True


class PhanHoiGioHang(BaseModel):
    items: List[PhanHoiGioHangItem]
    tong_so_luong: int
    tong_tien: float
