from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class DanhMucTao(BaseModel):
    ten: str
    mo_ta: Optional[str] = None
    anh: Optional[str] = None
    id_cha: Optional[int] = None
    dang_hoat_dong: bool = True


class DanhMucCapNhat(BaseModel):
    ten: Optional[str] = None
    mo_ta: Optional[str] = None
    anh: Optional[str] = None
    id_cha: Optional[int] = None
    dang_hoat_dong: Optional[bool] = None


class PhanHoiDanhMuc(BaseModel):
    id: int
    ten: str
    slug: str
    mo_ta: Optional[str] = None
    anh: Optional[str] = None
    id_cha: Optional[int] = None
    dang_hoat_dong: bool
    so_luong_san_pham: Optional[int] = 0
    con_cais: Optional[List["PhanHoiDanhMuc"]] = []
    ngay_tao: Optional[datetime] = None

    class Config:
        from_attributes = True


PhanHoiDanhMuc.model_rebuild()
