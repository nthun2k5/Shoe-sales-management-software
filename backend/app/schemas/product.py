from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class AnhSanPhamBase(BaseModel):
    du_lieu_anh: str
    la_anh_chinh: bool = False
    thu_tu_sap_xep: int = 0


class PhanHoiAnhSanPham(BaseModel):
    id: int
    du_lieu_anh: str
    la_anh_chinh: bool
    thu_tu_sap_xep: int

    class Config:
        from_attributes = True


class SanPhamTao(BaseModel):
    ten: str
    mo_ta: Optional[str] = None
    mo_ta_ngan: Optional[str] = None
    gia: float
    gia_khuyen_mai: Optional[float] = None
    so_luong_ton: int = 0
    ma_sku: Optional[str] = None
    id_danh_muc: Optional[int] = None
    thuong_hieu: Optional[str] = None
    dang_hoat_dong: bool = True
    la_noi_bat: bool = False
    cac_kich_thuoc: Optional[str] = None
    anh_san_phams: Optional[List[AnhSanPhamBase]] = []


class SanPhamCapNhat(BaseModel):
    ten: Optional[str] = None
    mo_ta: Optional[str] = None
    mo_ta_ngan: Optional[str] = None
    gia: Optional[float] = None
    gia_khuyen_mai: Optional[float] = None
    so_luong_ton: Optional[int] = None
    ma_sku: Optional[str] = None
    id_danh_muc: Optional[int] = None
    thuong_hieu: Optional[str] = None
    dang_hoat_dong: Optional[bool] = None
    la_noi_bat: Optional[bool] = None
    cac_kich_thuoc: Optional[str] = None


class PhanHoiSanPham(BaseModel):
    id: int
    ten: str
    slug: str
    mo_ta: Optional[str] = None
    mo_ta_ngan: Optional[str] = None
    gia: float
    gia_khuyen_mai: Optional[float] = None
    so_luong_ton: int
    ma_sku: Optional[str] = None
    id_danh_muc: Optional[int] = None
    thuong_hieu: Optional[str] = None
    dang_hoat_dong: bool
    la_noi_bat: bool
    cac_kich_thuoc: Optional[str] = None
    anh_san_phams: List[PhanHoiAnhSanPham] = []
    ten_danh_muc: Optional[str] = None
    diem_danh_gia_tb: Optional[float] = None
    so_luong_danh_gia: Optional[int] = 0
    ngay_tao: Optional[datetime] = None

    class Config:
        from_attributes = True


class PhanHoiDanhSachSanPham(BaseModel):
    items: List[PhanHoiSanPham]
    tong: int
    trang: int
    kich_thuoc_trang: int
    tong_so_trang: int
