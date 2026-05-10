from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PhuongThucThanhToanBase(BaseModel):
    ma_phuong_thuc: str
    ten_phuong_thuc: str
    mo_ta: Optional[str] = None
    icon_svg: Optional[str] = None
    anh_logo: Optional[str] = None
    kich_hoat: bool = True
    ho_tro_qr: bool = False

    # Phân loại & Thứ tự
    loai: str = "other"
    thu_tu: int = 0

    # Phí thanh toán
    phi_co_dinh: int = 0
    phi_phan_tram: int = 0

    # Quy tắc đơn hàng
    gia_tri_don_toi_thieu: Optional[int] = None
    gia_tri_don_toi_da: Optional[int] = None

    # Cấu hình API
    cau_hinh_json: Optional[str] = None


class TaoPhuongThucThanhToan(PhuongThucThanhToanBase):
    pass


class CapNhatPhuongThucThanhToan(BaseModel):
    ten_phuong_thuc: Optional[str] = None
    mo_ta: Optional[str] = None
    icon_svg: Optional[str] = None
    anh_logo: Optional[str] = None
    kich_hoat: Optional[bool] = None
    ho_tro_qr: Optional[bool] = None

    loai: Optional[str] = None
    thu_tu: Optional[int] = None
    phi_co_dinh: Optional[int] = None
    phi_phan_tram: Optional[int] = None
    gia_tri_don_toi_thieu: Optional[int] = None
    gia_tri_don_toi_da: Optional[int] = None
    cau_hinh_json: Optional[str] = None


class PhanHoiPhuongThucThanhToan(PhuongThucThanhToanBase):
    id: int
    ngay_tao: Optional[datetime] = None
    ngay_cap_nhat: Optional[datetime] = None

    class Config:
        from_attributes = True
