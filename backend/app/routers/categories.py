from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.configs.database import get_db
from app.models import DanhMuc, SanPham
from app.schemas import DanhMucTao, DanhMucCapNhat, PhanHoiDanhMuc
from app.utils.security import get_current_admin
from app.utils.helpers import generate_slug
from app.models import NguoiDung

router = APIRouter(prefix="/api/categories", tags=["Categories"])


def _build_danh_muc_response(dm: DanhMuc, db: Session) -> dict:
    so_luong_san_pham = db.query(SanPham).filter(SanPham.id_danh_muc == dm.id).count()
    con_cais = [_build_danh_muc_response(c, db) for c in (dm.con_cais or [])]
    return {
        "id": dm.id, "ten": dm.ten, "slug": dm.slug,
        "mo_ta": dm.mo_ta, "anh": dm.anh,
        "id_cha": dm.id_cha, "dang_hoat_dong": dm.dang_hoat_dong,
        "so_luong_san_pham": so_luong_san_pham, "con_cais": con_cais,
        "ngay_tao": dm.ngay_tao,
    }


@router.get("", response_model=List[PhanHoiDanhMuc])
def get_danh_mucs(db: Session = Depends(get_db)):
    danh_mucs = db.query(DanhMuc).filter(DanhMuc.id_cha == None).all()
    return [_build_danh_muc_response(dm, db) for dm in danh_mucs]


@router.get("/all", response_model=List[PhanHoiDanhMuc])
def get_all_danh_mucs(db: Session = Depends(get_db)):
    danh_mucs = db.query(DanhMuc).all()
    return [{
        "id": dm.id, "ten": dm.ten, "slug": dm.slug,
        "mo_ta": dm.mo_ta, "anh": dm.anh,
        "id_cha": dm.id_cha, "dang_hoat_dong": dm.dang_hoat_dong,
        "so_luong_san_pham": db.query(SanPham).filter(SanPham.id_danh_muc == dm.id).count(),
        "con_cais": [], "ngay_tao": dm.ngay_tao,
    } for dm in danh_mucs]


@router.get("/{danh_muc_id}", response_model=PhanHoiDanhMuc)
def get_danh_muc(danh_muc_id: int, db: Session = Depends(get_db)):
    dm = db.query(DanhMuc).filter(DanhMuc.id == danh_muc_id).first()
    if not dm:
        raise HTTPException(status_code=404, detail="Danh mục không tồn tại")
    return _build_danh_muc_response(dm, db)


@router.post("", response_model=PhanHoiDanhMuc)
def create_danh_muc(data: DanhMucTao, db: Session = Depends(get_db), admin: NguoiDung = Depends(get_current_admin)):
    slug = generate_slug(data.ten)
    existing = db.query(DanhMuc).filter(DanhMuc.slug == slug).first()
    if existing:
        slug = f"{slug}-{db.query(DanhMuc).count() + 1}"
    dm = DanhMuc(ten=data.ten, slug=slug, mo_ta=data.mo_ta, anh=data.anh, id_cha=data.id_cha, dang_hoat_dong=data.dang_hoat_dong)
    db.add(dm)
    db.commit()
    db.refresh(dm)
    return _build_danh_muc_response(dm, db)


@router.put("/{danh_muc_id}", response_model=PhanHoiDanhMuc)
def update_danh_muc(danh_muc_id: int, data: DanhMucCapNhat, db: Session = Depends(get_db), admin: NguoiDung = Depends(get_current_admin)):
    dm = db.query(DanhMuc).filter(DanhMuc.id == danh_muc_id).first()
    if not dm:
        raise HTTPException(status_code=404, detail="Danh mục không tồn tại")
    update_data = data.model_dump(exclude_unset=True)
    if "ten" in update_data:
        dm.slug = generate_slug(update_data["ten"])
    for key, value in update_data.items():
        setattr(dm, key, value)
    db.commit()
    db.refresh(dm)
    return _build_danh_muc_response(dm, db)


@router.delete("/{danh_muc_id}")
def delete_danh_muc(danh_muc_id: int, db: Session = Depends(get_db), admin: NguoiDung = Depends(get_current_admin)):
    dm = db.query(DanhMuc).filter(DanhMuc.id == danh_muc_id).first()
    if not dm:
        raise HTTPException(status_code=404, detail="Danh mục không tồn tại")
    pc = db.query(SanPham).filter(SanPham.id_danh_muc == danh_muc_id).count()
    if pc > 0:
        raise HTTPException(status_code=400, detail=f"Không thể xóa. Danh mục có {pc} sản phẩm")
    db.delete(dm)
    db.commit()
    return {"message": "Đã xóa danh mục"}
