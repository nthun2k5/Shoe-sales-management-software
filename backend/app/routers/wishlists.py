from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.configs.database import get_db
from app.models import DanhSachYeuThich, SanPham, NguoiDung
from app.schemas import PhanHoiSanPham
from app.utils.security import get_current_user

router = APIRouter(prefix="/api/wishlists", tags=["Wishlists"])


@router.get("")
def get_danh_sach_yeu_thich(db: Session = Depends(get_db), current_user: NguoiDung = Depends(get_current_user)):
    yeu_thichs = db.query(DanhSachYeuThich).filter(DanhSachYeuThich.id_nguoi_dung == current_user.id).all()
    result = []
    for yt in yeu_thichs:
        sp = yt.san_pham
        if sp:
            anh_chinh = None
            for img in sp.anh_san_phams:
                if img.la_anh_chinh:
                    anh_chinh = img.du_lieu_anh
                    break
            result.append({
                "id_yeu_thich": yt.id, "id_san_pham": sp.id,
                "ten": sp.ten, "slug": sp.slug,
                "gia": sp.gia, "gia_khuyen_mai": sp.gia_khuyen_mai,
                "anh_san_pham": anh_chinh, "ngay_tao": yt.ngay_tao
            })
    return result


@router.post("")
def them_vao_yeu_thich(data: dict, db: Session = Depends(get_db), current_user: NguoiDung = Depends(get_current_user)):
    id_san_pham = data.get("id_san_pham")
    san_pham = db.query(SanPham).filter(SanPham.id == id_san_pham).first()
    if not san_pham:
        raise HTTPException(status_code=404, detail="Sản phẩm không tồn tại")
    existing = db.query(DanhSachYeuThich).filter(
        DanhSachYeuThich.id_nguoi_dung == current_user.id,
        DanhSachYeuThich.id_san_pham == id_san_pham
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Sản phẩm đã trong danh sách yêu thích")
    db.add(DanhSachYeuThich(id_nguoi_dung=current_user.id, id_san_pham=id_san_pham))
    db.commit()
    return {"message": "Đã thêm vào yêu thích"}


@router.delete("/{id_san_pham}")
def xoa_khoi_yeu_thich(id_san_pham: int, db: Session = Depends(get_db), current_user: NguoiDung = Depends(get_current_user)):
    yt = db.query(DanhSachYeuThich).filter(
        DanhSachYeuThich.id_nguoi_dung == current_user.id,
        DanhSachYeuThich.id_san_pham == id_san_pham
    ).first()
    if not yt:
        raise HTTPException(status_code=404, detail="Không tìm thấy")
    db.delete(yt)
    db.commit()
    return {"message": "Đã xóa khỏi yêu thích"}


@router.get("/check/{id_san_pham}")
def check_yeu_thich(id_san_pham: int, db: Session = Depends(get_db), current_user: NguoiDung = Depends(get_current_user)):
    exists = db.query(DanhSachYeuThich).filter(
        DanhSachYeuThich.id_nguoi_dung == current_user.id,
        DanhSachYeuThich.id_san_pham == id_san_pham
    ).first()
    return {"la_yeu_thich": exists is not None}
