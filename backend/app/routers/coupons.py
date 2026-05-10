from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timezone

from app.configs.database import get_db
from app.models import MaGiamGia, SuDungMaGiamGia, NguoiDung
from app.schemas import CouponCreate, CouponUpdate, CouponResponse
from app.utils.security import get_current_user, get_current_admin

router = APIRouter(prefix="/api/coupons", tags=["Coupons"])


@router.get("", response_model=List[CouponResponse])
def get_coupons(
    db: Session = Depends(get_db),
    admin: NguoiDung = Depends(get_current_admin)
):
    """Lấy danh sách mã giảm giá (admin)."""
    return db.query(MaGiamGia).order_by(MaGiamGia.ngay_tao.desc()).all()


@router.get("/available")
def get_available_coupons(
    db: Session = Depends(get_db),
    current_user: NguoiDung = Depends(get_current_user)
):
    """Lấy danh sách mã giảm giá cho user hiện tại, kèm cờ _used."""
    now = datetime.now(timezone.utc)
    query = db.query(MaGiamGia).filter(
        MaGiamGia.dang_hoat_dong == True,
        (MaGiamGia.ngay_bat_dau == None) | (MaGiamGia.ngay_bat_dau <= now),
        (MaGiamGia.ngay_ket_thuc == None) | (MaGiamGia.ngay_ket_thuc >= now),
    )
    if current_user.vai_tro != "quan_tri":
        query = query.filter(
            (MaGiamGia.so_lan_su_dung_toi_da == 0) |
            (MaGiamGia.so_lan_da_su_dung < MaGiamGia.so_lan_su_dung_toi_da)
        )
    coupons = query.all()

    used_coupon_ids = set()
    if current_user.vai_tro != "quan_tri":
        used = db.query(SuDungMaGiamGia.id_ma_giam_gia).filter(
            SuDungMaGiamGia.id_nguoi_dung == current_user.id
        ).all()
        used_coupon_ids = {c[0] for c in used}

    result = []
    for c in coupons:
        d = {
            "id": c.id,
            "ma": c.ma,
            "loai_giam_gia": c.loai_giam_gia,
            "gia_tri_giam": c.gia_tri_giam,
            "gia_tri_don_toi_thieu": c.gia_tri_don_toi_thieu,
            "so_lan_su_dung_toi_da": c.so_lan_su_dung_toi_da,
            "so_lan_da_su_dung": c.so_lan_da_su_dung,
            "ngay_bat_dau": c.ngay_bat_dau,
            "ngay_ket_thuc": c.ngay_ket_thuc,
            "dang_hoat_dong": c.dang_hoat_dong,
            "ngay_tao": c.ngay_tao,
            "_used": c.id in used_coupon_ids,
        }
        result.append(d)
    return result


@router.post("", response_model=CouponResponse)
def create_coupon(
    data: CouponCreate,
    db: Session = Depends(get_db),
    admin: NguoiDung = Depends(get_current_admin)
):
    """Tạo mã giảm giá mới (admin)."""
    existing = db.query(MaGiamGia).filter(MaGiamGia.ma == data.ma).first()
    if existing:
        raise HTTPException(status_code=400, detail="Mã đã tồn tại")
    coupon = MaGiamGia(
        ma=data.ma,
        loai_giam_gia=data.loai_giam_gia,
        gia_tri_giam=data.gia_tri_giam,
        gia_tri_don_toi_thieu=data.gia_tri_don_toi_thieu,
        so_lan_su_dung_toi_da=data.so_lan_su_dung_toi_da,
        ngay_bat_dau=data.ngay_bat_dau,
        ngay_ket_thuc=data.ngay_ket_thuc,
        dang_hoat_dong=data.dang_hoat_dong,
    )
    db.add(coupon)
    db.commit()
    db.refresh(coupon)
    return coupon


@router.put("/{coupon_id}", response_model=CouponResponse)
def update_coupon(
    coupon_id: int,
    data: CouponUpdate,
    db: Session = Depends(get_db),
    admin: NguoiDung = Depends(get_current_admin)
):
    """Cập nhật mã giảm giá (admin)."""
    coupon = db.query(MaGiamGia).filter(MaGiamGia.id == coupon_id).first()
    if not coupon:
        raise HTTPException(status_code=404, detail="Mã không tồn tại")
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(coupon, key, value)
    db.commit()
    db.refresh(coupon)
    return coupon


@router.delete("/{coupon_id}")
def delete_coupon(
    coupon_id: int,
    db: Session = Depends(get_db),
    admin: NguoiDung = Depends(get_current_admin)
):
    """Xóa mã giảm giá (admin)."""
    coupon = db.query(MaGiamGia).filter(MaGiamGia.id == coupon_id).first()
    if not coupon:
        raise HTTPException(status_code=404, detail="Mã không tồn tại")
    db.delete(coupon)
    db.commit()
    return {"message": "Đã xóa mã giảm giá"}


@router.post("/validate")
def validate_coupon(
    data: dict,
    db: Session = Depends(get_db),
    current_user: NguoiDung = Depends(get_current_user)
):
    """Kiểm tra mã giảm giá có hợp lệ không (bao gồm kiểm tra user đã dùng chưa)."""
    ma = data.get("ma")
    tong_tien_don = data.get("tong_tien_don", 0)
    coupon = db.query(MaGiamGia).filter(
        MaGiamGia.ma == ma,
        MaGiamGia.dang_hoat_dong == True
    ).first()
    if not coupon:
        raise HTTPException(status_code=404, detail="Mã giảm giá không hợp lệ")
    now = datetime.now(timezone.utc)
    if coupon.ngay_bat_dau and now < coupon.ngay_bat_dau:
        raise HTTPException(status_code=400, detail="Mã giảm giá chưa có hiệu lực")
    if coupon.ngay_ket_thuc and now > coupon.ngay_ket_thuc:
        raise HTTPException(status_code=400, detail="Mã giảm giá đã hết hạn")
    if coupon.so_lan_su_dung_toi_da > 0 and coupon.so_lan_da_su_dung >= coupon.so_lan_su_dung_toi_da:
        raise HTTPException(status_code=400, detail="Mã đã hết lượt sử dụng")
    if tong_tien_don < coupon.gia_tri_don_toi_thieu:
        raise HTTPException(status_code=400, detail=f"Đơn hàng tối thiểu {coupon.gia_tri_don_toi_thieu:,.0f}₫")
    used = db.query(SuDungMaGiamGia).filter(
        SuDungMaGiamGia.id_nguoi_dung == current_user.id,
        SuDungMaGiamGia.id_ma_giam_gia == coupon.id
    ).first()
    if used:
        raise HTTPException(status_code=400, detail="Bạn đã sử dụng mã này rồi")
    tien_giam = coupon.gia_tri_giam if coupon.loai_giam_gia == "co_dinh" else tong_tien_don * coupon.gia_tri_giam / 100
    return {
        "hop_le": True,
        "loai_giam_gia": coupon.loai_giam_gia,
        "gia_tri_giam": coupon.gia_tri_giam,
        "so_tien_giam": tien_giam
    }
