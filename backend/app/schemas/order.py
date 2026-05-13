from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class ChiTietDonHangTao(BaseModel):
    id_san_pham: int
    so_luong: int


class PhanHoiChiTietDonHang(BaseModel):
    id: int
    id_san_pham: int
    ten_san_pham: Optional[str] = None
    anh_san_pham: Optional[str] = None
    kich_thuoc: Optional[str] = None
    so_luong: int
    don_gia: float
    thanh_tien: float

    class Config:
        from_attributes = True


class PhanHoiLichSuDonHang(BaseModel):
    id: int
    hanh_dong: str
    mo_ta: Optional[str] = None
    ngay_tao: datetime
    nguoi_dung: Optional[str] = None

    class Config:
        from_attributes = True


class DonHangTao(BaseModel):
    chi_tiet_don_hangs: Optional[List[ChiTietDonHangTao]] = None
    ten_nguoi_nhan: str
    sdt_nguoi_nhan: str
    dia_chi_nhan: str
    phuong_thuc_thanh_toan: str
    ghi_chu: Optional[str] = None
    ma_giam_gia: Optional[str] = None


class DonHangCapNhatTrangThai(BaseModel):
    trang_thai: Optional[str] = None
    ghi_chu: Optional[str] = None


class PhanHoiDonHang(BaseModel):
    id: int
    ma_don_hang: str
    id_nguoi_dung: int
    ten_nguoi_dung: Optional[str] = None
    tong_tien: float
    tien_giam_gia: float
    phi_van_chuyen: float
    thanh_tien: float
    trang_thai: str
    phuong_thuc_thanh_toan: Optional[str] = None
    trang_thai_thanh_toan: str
    ten_nguoi_nhan: Optional[str] = None
    sdt_nguoi_nhan: Optional[str] = None
    dia_chi_nhan: Optional[str] = None
    ghi_chu: Optional[str] = None
    chi_tiet_don_hangs: List[PhanHoiChiTietDonHang] = []
    lich_su_tac_dong: List[PhanHoiLichSuDonHang] = []
    ngay_tao: Optional[datetime] = None

    class Config:
        from_attributes = True


class PhanHoiDanhSachDonHang(BaseModel):
    items: List[PhanHoiDonHang]
    tong: int
    trang: int
    kich_thuoc_trang: int
