from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.configs.database import get_db
from app.models import GioHang, SanPham, NguoiDung
from app.schemas import GioHangThem, GioHangCapNhat, PhanHoiGioHang, PhanHoiGioHangItem
from app.utils.security import get_current_user

router = APIRouter(prefix="/api/cart", tags=["Cart"])


def _get_gio_hang_response(id_nguoi_dung: int, db: Session) -> PhanHoiGioHang:
    gio_hangs = db.query(GioHang).filter(GioHang.id_nguoi_dung == id_nguoi_dung).all()
    items = []
    tong_tien = 0.0
    for item in gio_hangs:
        san_pham = item.san_pham
        if not san_pham:
            continue
        gia = san_pham.gia_khuyen_mai or san_pham.gia
        thanh_tien = gia * item.so_luong
        tong_tien += thanh_tien
        anh_chinh = None
        for img in san_pham.anh_san_phams:
            if img.la_anh_chinh:
                anh_chinh = img.du_lieu_anh
                break
        items.append(PhanHoiGioHangItem(
            id=item.id, id_san_pham=item.id_san_pham,
            ten_san_pham=san_pham.ten, anh_san_pham=anh_chinh,
            gia_san_pham=san_pham.gia, gia_khuyen_mai=san_pham.gia_khuyen_mai,
            kich_thuoc=item.kich_thuoc,
            so_luong=item.so_luong, thanh_tien=thanh_tien
        ))
    return PhanHoiGioHang(items=items, tong_so_luong=len(items), tong_tien=tong_tien)


@router.get("", response_model=PhanHoiGioHang)
def get_gio_hang(db: Session = Depends(get_db), current_user: NguoiDung = Depends(get_current_user)):
    return _get_gio_hang_response(current_user.id, db)


@router.post("", response_model=PhanHoiGioHang)
def them_vao_gio_hang(data: GioHangThem, db: Session = Depends(get_db), current_user: NguoiDung = Depends(get_current_user)):
    san_pham = db.query(SanPham).filter(SanPham.id == data.id_san_pham, SanPham.dang_hoat_dong == True).first()
    if not san_pham:
        raise HTTPException(status_code=404, detail="Sản phẩm không tồn tại")
    existing = db.query(GioHang).filter(
        GioHang.id_nguoi_dung == current_user.id, 
        GioHang.id_san_pham == data.id_san_pham,
        GioHang.kich_thuoc == data.kich_thuoc
    ).first()
    if existing:
        existing.so_luong += data.so_luong
    else:
        db.add(GioHang(id_nguoi_dung=current_user.id, id_san_pham=data.id_san_pham, kich_thuoc=data.kich_thuoc, so_luong=data.so_luong))
    db.commit()
    return _get_gio_hang_response(current_user.id, db)


@router.put("/{gio_hang_id}", response_model=PhanHoiGioHang)
def update_gio_hang(gio_hang_id: int, data: GioHangCapNhat, db: Session = Depends(get_db), current_user: NguoiDung = Depends(get_current_user)):
    item = db.query(GioHang).filter(GioHang.id == gio_hang_id, GioHang.id_nguoi_dung == current_user.id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Không tìm thấy")
    if data.so_luong <= 0:
        db.delete(item)
    else:
        item.so_luong = data.so_luong
    db.commit()
    return _get_gio_hang_response(current_user.id, db)


@router.delete("/{gio_hang_id}", response_model=PhanHoiGioHang)
def xoa_khoi_gio_hang(gio_hang_id: int, db: Session = Depends(get_db), current_user: NguoiDung = Depends(get_current_user)):
    item = db.query(GioHang).filter(GioHang.id == gio_hang_id, GioHang.id_nguoi_dung == current_user.id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Không tìm thấy")
    db.delete(item)
    db.commit()
    return _get_gio_hang_response(current_user.id, db)


@router.delete("")
def xoa_het_gio_hang(db: Session = Depends(get_db), current_user: NguoiDung = Depends(get_current_user)):
    db.query(GioHang).filter(GioHang.id_nguoi_dung == current_user.id).delete()
    db.commit()
    return {"message": "Đã xóa giỏ hàng"}
