from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class NganHangBase(BaseModel):
    loai: str = "ngan_hang"  # "ngan_hang" or "vi_dien_tu"
    ten_ngan_hang: str
    ma_ngan_hang: Optional[str] = None
    chu_tai_khoan: Optional[str] = None
    so_tai_khoan: Optional[str] = None
    so_dien_thoai: Optional[str] = None
    chi_nhanh: Optional[str] = None
    dang_su_dung: bool = True


class NganHangTao(NganHangBase):
    pass


class NganHangCapNhat(BaseModel):
    loai: Optional[str] = None
    ten_ngan_hang: Optional[str] = None
    ma_ngan_hang: Optional[str] = None
    chu_tai_khoan: Optional[str] = None
    so_tai_khoan: Optional[str] = None
    so_dien_thoai: Optional[str] = None
    chi_nhanh: Optional[str] = None
    dang_su_dung: Optional[bool] = None


class NganHangPhanHoi(NganHangBase):
    id: int
    ngay_tao: datetime
    ngay_cap_nhat: datetime

    class Config:
        from_attributes = True
