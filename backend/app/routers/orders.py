import math
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func as sql_func
from typing import Optional, List
from datetime import datetime, timezone

from app.configs.database import get_db
from app.models import DonHang, ChiTietDonHang, SanPham, AnhSanPham, NguoiDung, MaGiamGia, ThanhToan, GioHang, NhatKy, SuDungMaGiamGia
from app.schemas import (
    DonHangTao, DonHangCapNhatTrangThai, PhanHoiDonHang,
    PhanHoiDanhSachDonHang, ChiTietDonHangTao
)
from app.utils.security import get_current_user, get_current_admin
from app.utils.helpers import generate_order_code
from app.utils.logger import log_activity

router = APIRouter(prefix="/api/orders", tags=["Orders"])


def _build_don_hang_response(don_hang: DonHang, db: Session) -> dict:
    ten_nguoi_dung = don_hang.nguoi_dung.ho_ten if don_hang.nguoi_dung else None
    chi_tiet = []
    for item in don_hang.chi_tiet_don_hangs:
        ten_san_pham = item.san_pham.ten if item.san_pham else None
        anh_chinh = None
        if item.san_pham:
            for img in item.san_pham.anh_san_phams:
                if img.la_anh_chinh:
                    anh_chinh = img.du_lieu_anh
                    break
        chi_tiet.append({
            "id": item.id,
            "id_san_pham": item.id_san_pham,
            "ten_san_pham": ten_san_pham,
            "anh_san_pham": anh_chinh,
            "kich_thuoc": item.kich_thuoc,
            "so_luong": item.so_luong,
            "don_gia": item.don_gia,
            "thanh_tien": item.thanh_tien,
        })
        
    nhat_ky_entries = db.query(NhatKy).filter(NhatKy.id_don_hang == don_hang.id).order_by(NhatKy.ngay_tao.desc()).all()
    lich_su = []
    for entry in nhat_ky_entries:
        nguoi_dung = entry.nguoi_dung.ho_ten if entry.nguoi_dung else "Hệ thống"
        lich_su.append({
            "id": entry.id,
            "hanh_dong": entry.hanh_dong,
            "mo_ta": entry.mo_ta,
            "ngay_tao": entry.ngay_tao,
            "nguoi_dung": nguoi_dung
        })
        
    return {
        "id": don_hang.id,
        "ma_don_hang": don_hang.ma_don_hang,
        "id_nguoi_dung": don_hang.id_nguoi_dung,
        "ten_nguoi_dung": ten_nguoi_dung,
        "tong_tien": don_hang.tong_tien,
        "tien_giam_gia": don_hang.tien_giam_gia,
        "phi_van_chuyen": don_hang.phi_van_chuyen,
        "thanh_tien": don_hang.thanh_tien,
        "trang_thai": don_hang.trang_thai,
        "phuong_thuc_thanh_toan": don_hang.phuong_thuc_thanh_toan,
        "trang_thai_thanh_toan": don_hang.trang_thai_thanh_toan,
        "ten_nguoi_nhan": don_hang.ten_nguoi_nhan,
        "sdt_nguoi_nhan": don_hang.sdt_nguoi_nhan,
        "dia_chi_nhan": don_hang.dia_chi_nhan,
        "ghi_chu": don_hang.ghi_chu,
        "chi_tiet_don_hangs": chi_tiet,
        "lich_su_tac_dong": lich_su,
        "ngay_tao": don_hang.ngay_tao,
    }


@router.get("/my", response_model=PhanHoiDanhSachDonHang)
def get_my_orders(
    trang: int = 1,
    kich_thuoc_trang: int = 10,
    db: Session = Depends(get_db),
    current_user: NguoiDung = Depends(get_current_user)
):
    """Lấy đơn hàng của tôi."""
    query = db.query(DonHang).filter(DonHang.id_nguoi_dung == current_user.id)
    query = query.order_by(DonHang.ngay_tao.desc())
    total = query.count()
    items = query.offset((trang -1) * kich_thuoc_trang).limit(kich_thuoc_trang).all()
    return PhanHoiDanhSachDonHang(
        items=[_build_don_hang_response(dh, db) for dh in items],
        tong=total, trang=trang, kich_thuoc_trang=kich_thuoc_trang
    )


@router.post("", response_model=PhanHoiDonHang)
def create_don_hang(
    data: DonHangTao,
    db: Session = Depends(get_db),
    current_user: NguoiDung = Depends(get_current_user)
):
    """Tạo đơn hàng mới."""
    ma_don_hang = generate_order_code()
    chi_tiet_don_hangs = []
    tong_tien = 0.0

    if data.chi_tiet_don_hangs:
        for item in data.chi_tiet_don_hangs:
            san_pham = db.query(SanPham).filter(SanPham.id == item.id_san_pham).first()
            if not san_pham:
                raise HTTPException(status_code=404, detail=f"Sản phẩm {item.id_san_pham} không tồn tại")
            if san_pham.so_luong_ton < item.so_luong:
                raise HTTPException(status_code=400, detail=f"Sản phẩm {san_pham.ten} không đủ số lượng")
            don_gia = san_pham.gia_khuyen_mai or san_pham.gia
            thanh_tien = don_gia * item.so_luong
            tong_tien += thanh_tien
            chi_tiet_don_hangs.append({
                "id_san_pham": item.id_san_pham,
                "so_luong": item.so_luong,
                "don_gia": don_gia,
                "thanh_tien": thanh_tien,
            })
            san_pham.so_luong_ton -= item.so_luong
    else:
        gio_hangs = db.query(GioHang).filter(GioHang.id_nguoi_dung == current_user.id).all()
        if not gio_hangs:
            raise HTTPException(status_code=400, detail="Giỏ hàng trống")
        for item in gio_hangs:
            san_pham = item.san_pham
            if san_pham.so_luong_ton < item.so_luong:
                raise HTTPException(status_code=400, detail=f"Sản phẩm {san_pham.ten} không đủ số lượng")
            don_gia = san_pham.gia_khuyen_mai or san_pham.gia
            thanh_tien = don_gia * item.so_luong
            tong_tien += thanh_tien
            chi_tiet_don_hangs.append({
                "id_san_pham": item.id_san_pham,
                "so_luong": item.so_luong,
                "don_gia": don_gia,
                "thanh_tien": thanh_tien,
            })
            san_pham.so_luong_ton -= item.so_luong

    tien_giam_gia = 0.0
    coupon_id_used = None
    if data.ma_giam_gia:
        ma_giam_gia = db.query(MaGiamGia).filter(MaGiamGia.ma == data.ma_giam_gia, MaGiamGia.dang_hoat_dong == True).first()
        if ma_giam_gia:
            now = datetime.now(timezone.utc)
            if ma_giam_gia.ngay_bat_dau and now < ma_giam_gia.ngay_bat_dau:
                raise HTTPException(status_code=400, detail="Mã giảm giá chưa có hiệu lực")
            if ma_giam_gia.ngay_ket_thuc and now > ma_giam_gia.ngay_ket_thuc:
                raise HTTPException(status_code=400, detail="Mã giảm giá đã hết hạn")
            if ma_giam_gia.so_lan_su_dung_toi_da > 0 and ma_giam_gia.so_lan_da_su_dung >= ma_giam_gia.so_lan_su_dung_toi_da:
                raise HTTPException(status_code=400, detail="Mã giảm giá đã hết lượt sử dụng")
            if tong_tien < ma_giam_gia.gia_tri_don_toi_thieu:
                raise HTTPException(status_code=400, detail=f"Đơn hàng tối thiểu {ma_giam_gia.gia_tri_don_toi_thieu:,.0f}₫")
            used = db.query(SuDungMaGiamGia).filter(
                SuDungMaGiamGia.id_nguoi_dung == current_user.id,
                SuDungMaGiamGia.id_ma_giam_gia == ma_giam_gia.id
            ).first()
            if used:
                raise HTTPException(status_code=400, detail="Bạn đã sử dụng mã này rồi")
            if ma_giam_gia.loai_giam_gia == "phan_tram":
                tien_giam_gia = tong_tien * ma_giam_gia.gia_tri_giam / 100
            else:
                tien_giam_gia = ma_giam_gia.gia_tri_giam
            ma_giam_gia.so_lan_da_su_dung += 1
            coupon_id_used = ma_giam_gia.id

    phi_van_chuyen = 30000.0 if tong_tien < 500000 else 0.0
    thanh_tien = tong_tien - tien_giam_gia + phi_van_chuyen

    don_hang = DonHang(
        id_nguoi_dung=current_user.id,
        ma_don_hang=ma_don_hang,
        tong_tien=tong_tien,
        tien_giam_gia=tien_giam_gia,
        phi_van_chuyen=phi_van_chuyen,
        thanh_tien=thanh_tien,
        ten_nguoi_nhan=data.ten_nguoi_nhan,
        sdt_nguoi_nhan=data.sdt_nguoi_nhan,
        dia_chi_nhan=data.dia_chi_nhan,
        phuong_thuc_thanh_toan=data.phuong_thuc_thanh_toan,
        ghi_chu=data.ghi_chu,
    )
    db.add(don_hang)
    db.flush()

    for item_data in chi_tiet_don_hangs:
        chi_tiet = ChiTietDonHang(
            id_don_hang=don_hang.id,
            id_san_pham=item_data["id_san_pham"],
            so_luong=item_data["so_luong"],
            don_gia=item_data["don_gia"],
            thanh_tien=item_data["thanh_tien"],
        )
        db.add(chi_tiet)

    db.add(ThanhToan(id_don_hang=don_hang.id, phuong_thuc=data.phuong_thuc_thanh_toan, so_tien=thanh_tien, trang_thai="cho_xu_ly"))

    if not data.chi_tiet_don_hangs:
        db.query(GioHang).filter(GioHang.id_nguoi_dung == current_user.id).delete()

    db.commit()
    db.refresh(don_hang)

    # Record coupon usage
    if coupon_id_used:
        usage = SuDungMaGiamGia(id_nguoi_dung=current_user.id, id_ma_giam_gia=coupon_id_used)
        db.add(usage)
        db.commit()

    # Log activity
    log_activity(db, "ORDER_CREATE", f"Đã tạo đơn hàng mới {don_hang.ma_don_hang}", current_user.id, id_don_hang=don_hang.id)

    return _build_don_hang_response(don_hang, db)


@router.get("/{don_hang_id}", response_model=PhanHoiDonHang)
def get_don_hang(
    don_hang_id: int,
    db: Session = Depends(get_db),
    current_user: NguoiDung = Depends(get_current_user)
):
    """Lấy chi tiết đơn hàng."""
    don_hang = db.query(DonHang).filter(DonHang.id == don_hang_id).first()
    if not don_hang:
        raise HTTPException(status_code=404, detail="Đơn hàng không tồn tại")
    if don_hang.id_nguoi_dung != current_user.id and current_user.vai_tro != "quan_tri":
        raise HTTPException(status_code=403, detail="Không có quyền truy cập")
    return _build_don_hang_response(don_hang, db)


@router.put("/{don_hang_id}/status")
def update_don_hang_status(
    don_hang_id: int,
    data: DonHangCapNhatTrangThai,
    db: Session = Depends(get_db),
    admin: NguoiDung = Depends(get_current_admin)
):
    """Cập nhật trạng thái đơn hàng (admin)."""
    don_hang = db.query(DonHang).filter(DonHang.id == don_hang_id).first()
    if not don_hang:
        raise HTTPException(status_code=404, detail="Đơn hàng không tồn tại")
    
    # Define status order/priority
    status_priority = {
        "cho_xu_ly": 1,
        "da_xac_nhan": 2,
        "dang_giao": 3,
        "da_giao": 4,
        "da_huy": 5
    }

    current_p = status_priority.get(don_hang.trang_thai, 0)
    new_p = status_priority.get(data.trang_thai, 0)

    if don_hang.trang_thai == "da_giao":
        raise HTTPException(status_code=400, detail="Đơn hàng đã giao thành công, không thể thay đổi trạng thái")
    
    if don_hang.trang_thai == "da_huy":
        raise HTTPException(status_code=400, detail="Đơn hàng đã hủy, không thể thay đổi trạng thái")

    if new_p <= current_p and data.trang_thai != don_hang.trang_thai:
        raise HTTPException(status_code=400, detail="Không thể cập nhật lùi trạng thái đơn hàng")
    
    status_messages = {
        "da_xac_nhan": "Đơn hàng đã được xác nhận. Shop sẽ sớm xử lý và chuyển hàng đến bạn.",
        "dang_giao": "Đơn hàng đang trên đường giao đến bạn. Vui lòng để ý điện thoại để nhận hàng.",
        "da_giao": "Đơn hàng đã giao thành công. Cảm ơn bạn đã mua hàng! Đừng quên để lại đánh giá nhé.",
        "da_huy": data.ghi_chu if data.ghi_chu else "Đơn hàng đã bị hủy bởi shop."
    }

    # If cancelling, require a reason
    if data.trang_thai == "da_huy" and not data.ghi_chu:
        raise HTTPException(status_code=400, detail="Vui lòng điền lý do hủy đơn hàng")

    if not data.trang_thai:
        raise HTTPException(status_code=400, detail="Thiếu trạng thái đơn hàng")

    mo_ta_log = status_messages.get(data.trang_thai, f"Cập nhật trạng thái đơn hàng thành {data.trang_thai}")
    
    don_hang.trang_thai = data.trang_thai
    if data.ghi_chu:
        don_hang.ghi_chu = data.ghi_chu

    if data.trang_thai == "da_giao":
        don_hang.trang_thai_thanh_toan = "da_thanh_toan"
        thanh_toan = db.query(ThanhToan).filter(ThanhToan.id_don_hang == don_hang.id).first()
        if thanh_toan:
            thanh_toan.trang_thai = "da_hoan_thanh"
            thanh_toan.thoi_diem_thanh_toan = datetime.now(timezone.utc)
    
    if data.trang_thai == "da_huy":
        for item in don_hang.chi_tiet_don_hangs:
            san_pham = db.query(SanPham).filter(SanPham.id == item.id_san_pham).first()
            if san_pham:
                san_pham.so_luong_ton += item.so_luong

    db.commit()
    
    # Log activity with specific status as action
    log_activity(db, data.trang_thai, mo_ta_log, admin.id, id_don_hang=don_hang.id)
    
    return {"message": "Đã cập nhật trạng thái đơn hàng"}


@router.put("/{don_hang_id}/cancel")
def cancel_don_hang(
    don_hang_id: int,
    data: Optional[DonHangCapNhatTrangThai] = None,
    db: Session = Depends(get_db),
    current_user: NguoiDung = Depends(get_current_user)
):
    """Hủy đơn hàng."""
    don_hang = db.query(DonHang).filter(DonHang.id == don_hang_id).first()
    if not don_hang:
        raise HTTPException(status_code=404, detail="Đơn hàng không tồn tại")
    if don_hang.id_nguoi_dung != current_user.id and current_user.vai_tro != "quan_tri":
        raise HTTPException(status_code=403, detail="Không có quyền")
    if don_hang.trang_thai not in ["cho_xu_ly", "da_xac_nhan"]:
        raise HTTPException(status_code=400, detail="Không thể hủy đơn hàng này")
    
    ly_do_huy = "Hủy mua từ khách hàng"
    if data and data.ghi_chu:
        ly_do_huy = data.ghi_chu
    elif current_user.vai_tro == "quan_tri":
        # Admin cancels must have a reason (if using this endpoint)
        if not data or not data.ghi_chu:
            raise HTTPException(status_code=400, detail="Vui lòng điền lý do hủy đơn hàng")
        ly_do_huy = data.ghi_chu

    don_hang.trang_thai = "da_huy"
    don_hang.ghi_chu = ly_do_huy
    
    for item in don_hang.chi_tiet_don_hangs:
        san_pham = db.query(SanPham).filter(SanPham.id == item.id_san_pham).first()
        if san_pham:
            san_pham.so_luong_ton += item.so_luong
    db.commit()
    
    # Log activity
    log_activity(db, "da_huy", ly_do_huy, current_user.id, id_don_hang=don_hang.id)
    
    return {"message": "Đã hủy đơn hàng"}


@router.post("/{don_hang_id}/confirm-payment")
def confirm_payment(
    don_hang_id: int,
    db: Session = Depends(get_db),
    current_user: NguoiDung = Depends(get_current_user)
):
    """Xác nhận đã thanh toán (người dùng)."""
    don_hang = db.query(DonHang).filter(DonHang.id == don_hang_id, DonHang.id_nguoi_dung == current_user.id).first()
    if not don_hang:
        raise HTTPException(status_code=404, detail="Đơn hàng không tồn tại")
    
    don_hang.trang_thai_thanh_toan = "da_thanh_toan"
    # Also update the order status to 'da_xac_nhan' if it was 'cho_xu_ly'
    if don_hang.trang_thai == "cho_xu_ly":
        don_hang.trang_thai = "da_xac_nhan"

    thanh_toan = db.query(ThanhToan).filter(ThanhToan.id_don_hang == don_hang.id).first()
    if thanh_toan:
        thanh_toan.trang_thai = "da_hoan_thanh"
        thanh_toan.thoi_diem_thanh_toan = datetime.now(timezone.utc)
    
    db.commit()
    
    # Log activity
    log_activity(db, "PAYMENT_CONFIRM", f"Khách hàng xác nhận đã thanh toán cho đơn hàng {don_hang.ma_don_hang}. Trạng thái đơn hàng chuyển thành Đã xác nhận.", current_user.id, id_don_hang=don_hang.id)
    
    return {"message": "Đã xác nhận thanh toán"}


@router.get("", response_model=PhanHoiDanhSachDonHang)
def get_all_don_hangs(
    trang: int = 1,
    kich_thuoc_trang: int = 20,
    trang_thai: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    admin: NguoiDung = Depends(get_current_admin)
):
    """Lấy tất cả đơn hàng (admin)."""
    query = db.query(DonHang)
    if trang_thai:
        query = query.filter(DonHang.trang_thai == trang_thai)
    if search:
        query = query.filter(DonHang.ma_don_hang.ilike(f"%{search}%"))
    query = query.order_by(DonHang.ngay_tao.desc())
    total = query.count()
    items = query.offset((trang -1) * kich_thuoc_trang).limit(kich_thuoc_trang).all()
    return PhanHoiDanhSachDonHang(
        items=[_build_don_hang_response(dh, db) for dh in items],
        tong=total, trang=trang, kich_thuoc_trang=kich_thuoc_trang
    )
