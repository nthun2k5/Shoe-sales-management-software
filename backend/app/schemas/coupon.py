from pydantic import BaseModel, validator
from typing import Optional, List
from datetime import datetime


class CouponBase(BaseModel):
    ma: str
    loai_giam_gia: str
    gia_tri_giam: float
    gia_tri_don_toi_thieu: float = 0
    so_lan_su_dung_toi_da: int = 0
    ngay_bat_dau: Optional[datetime] = None
    ngay_ket_thuc: Optional[datetime] = None
    dang_hoat_dong: bool = True

    @validator('loai_giam_gia')
    def validate_loai(cls, v):
        if v not in ('phan_tram', 'co_dinh'):
            raise ValueError('loai_giam_gia must be phan_tram or co_dinh')
        return v


class CouponCreate(CouponBase):
    pass


class CouponUpdate(BaseModel):
    loai_giam_gia: Optional[str] = None
    gia_tri_giam: Optional[float] = None
    gia_tri_don_toi_thieu: Optional[float] = None
    so_lan_su_dung_toi_da: Optional[int] = None
    ngay_bat_dau: Optional[datetime] = None
    ngay_ket_thuc: Optional[datetime] = None
    dang_hoat_dong: Optional[bool] = None


class CouponUsage(BaseModel):
    id: int
    id_nguoi_dung: int
    id_ma_giam_gia: int
    ngay_su_dung: datetime

    class Config:
        from_attributes = True


class CouponResponse(CouponBase):
    id: int
    so_lan_da_su_dung: int
    ngay_tao: datetime

    class Config:
        from_attributes = True
