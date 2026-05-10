from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


# --- Auth Schemas ---
class NguoiDungDangKy(BaseModel):
    email: EmailStr
    mat_khau: str
    ho_ten: str
    so_dien_thoai: Optional[str] = None


class NguoiDungDangNhap(BaseModel):
    email: EmailStr
    mat_khau: str


class PhanHoiToken(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    nguoi_dung: "PhanHoiNguoiDung"


class YeCauRefreshToken(BaseModel):
    refresh_token: str


# --- User Schemas ---
class NguoiDungBase(BaseModel):
    email: EmailStr
    ho_ten: str
    so_dien_thoai: Optional[str] = None
    dia_chi: Optional[str] = None


class NguoiDungTao(NguoiDungBase):
    mat_khau: str
    vai_tro: Optional[str] = "khach"


class NguoiDungCapNhat(BaseModel):
    ho_ten: Optional[str] = None
    so_dien_thoai: Optional[str] = None
    dia_chi: Optional[str] = None
    vai_tro: Optional[str] = None


class NguoiDungDoiMatKhau(BaseModel):
    mat_khau_hien_tai: str
    mat_khau_moi: str


class PhanHoiNguoiDung(BaseModel):
    id: int
    email: str
    ho_ten: str
    so_dien_thoai: Optional[str] = None
    dia_chi: Optional[str] = None
    vai_tro: str
    anh_dai_dien: Optional[str] = None
    dang_hoat_dong: bool
    ngay_tao: Optional[datetime] = None

    class Config:
        from_attributes = True


# Rebuild to resolve forward ref
PhanHoiToken.model_rebuild()
