from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.configs.database import get_db
from app.models import DanhGia, SanPham, NguoiDung
from app.utils.security import get_current_user, get_current_admin

router = APIRouter(prefix="/api/reviews", tags=["Reviews"])


@router.post("")
def create_danh_gia(data: dict, db: Session = Depends(get_db), current_user: NguoiDung = Depends(get_current_user)):
    id_san_pham = data.get("id_san_pham")
    san_pham = db.query(SanPham).filter(SanPham.id == id_san_pham).first()
    if not san_pham:
        raise HTTPException(status_code=404, detail="Sản phẩm không tồn tại")
    existing = db.query(DanhGia).filter(
        DanhGia.id_nguoi_dung == current_user.id,
        DanhGia.id_san_pham == id_san_pham
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Bạn đã đánh giá sản phẩm này")
    diem = data.get("diem_danh_gia", 5)
    if diem < 1 or diem > 5:
        raise HTTPException(status_code=400, detail="Điểm đánh giá phải từ 1-5")
    danh_gia = DanhGia(
        id_nguoi_dung=current_user.id,
        id_san_pham=id_san_pham,
        diem_danh_gia=diem,
        binh_luan=data.get("binh_luan")
    )
    db.add(danh_gia)
    db.commit()
    db.refresh(danh_gia)
    return {
        "id": danh_gia.id, "diem_danh_gia": danh_gia.diem_danh_gia,
        "binh_luan": danh_gia.binh_luan, "ho_ten": current_user.ho_ten,
        "ngay_tao": str(danh_gia.ngay_tao)
    }


@router.get("/san-pham/{id_san_pham}")
def get_danh_gia_san_pham(id_san_pham: int, db: Session = Depends(get_db)):
    danh_gias = db.query(DanhGia).filter(DanhGia.id_san_pham == id_san_pham).order_by(DanhGia.ngay_tao.desc()).all()
    result = []
    for dg in danh_gias:
        nd = db.query(NguoiDung).filter(NguoiDung.id == dg.id_nguoi_dung).first()
        result.append({
            "id": dg.id, "diem_danh_gia": dg.diem_danh_gia, "binh_luan": dg.binh_luan,
            "ho_ten": nd.ho_ten if nd else "Ẩn danh",
            "anh_dai_dien": nd.anh_dai_dien if nd else None,
            "ngay_tao": str(dg.ngay_tao)
        })
    return result


@router.delete("/{danh_gia_id}")
def delete_danh_gia(danh_gia_id: int, db: Session = Depends(get_db), admin: NguoiDung = Depends(get_current_admin)):
    danh_gia = db.query(DanhGia).filter(DanhGia.id == danh_gia_id).first()
    if not danh_gia:
        raise HTTPException(status_code=404, detail="Đánh giá không tồn tại")
    db.delete(danh_gia)
    db.commit()
    return {"message": "Đã xóa đánh giá"}
