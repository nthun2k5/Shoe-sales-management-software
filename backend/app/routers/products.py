import math
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func as sql_func
from typing import Optional

from app.configs.database import get_db
from app.models import SanPham, AnhSanPham, DanhMuc, DanhGia
from app.schemas import (
    SanPhamTao, SanPhamCapNhat, PhanHoiSanPham,
    PhanHoiDanhSachSanPham, AnhSanPhamBase
)
from app.utils.security import get_current_admin, get_current_user
from app.utils.helpers import generate_slug
from app.utils.logger import log_activity

router = APIRouter(prefix="/api/products", tags=["Products"])


def _build_san_pham_response(san_pham: SanPham, db: Session) -> dict:
    """Build product response with computed fields."""
    avg_rating = db.query(sql_func.avg(DanhGia.diem_danh_gia)).filter(DanhGia.id_san_pham == san_pham.id).scalar()
    review_count = db.query(sql_func.count(DanhGia.id)).filter(DanhGia.id_san_pham == san_pham.id).scalar()
    ten_danh_muc = None
    if san_pham.danh_muc:
        ten_danh_muc = san_pham.danh_muc.ten
    return {
        "id": san_pham.id,
        "ten": san_pham.ten,
        "slug": san_pham.slug,
        "mo_ta": san_pham.mo_ta,
        "mo_ta_ngan": san_pham.mo_ta_ngan,
        "gia": san_pham.gia,
        "gia_khuyen_mai": san_pham.gia_khuyen_mai,
        "so_luong_ton": san_pham.so_luong_ton,
        "ma_sku": san_pham.ma_sku,
        "id_danh_muc": san_pham.id_danh_muc,
        "thuong_hieu": san_pham.thuong_hieu,
        "dang_hoat_dong": san_pham.dang_hoat_dong,
        "la_noi_bat": san_pham.la_noi_bat,
        "cac_kich_thuoc": san_pham.cac_kich_thuoc,
        "anh_san_phams": san_pham.anh_san_phams,
        "ten_danh_muc": ten_danh_muc,
        "diem_danh_gia_tb": round(float(avg_rating), 1) if avg_rating else None,
        "so_luong_danh_gia": review_count or 0,
        "ngay_tao": san_pham.ngay_tao,
    }


@router.get("", response_model=PhanHoiDanhSachSanPham)
def get_san_phams(
    page: int = Query(1, ge=1),
    page_size: int = Query(12, ge=1, le=100),
    search: Optional[str] = None,
    id_danh_muc: Optional[int] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    la_noi_bat: Optional[bool] = None,
    sort_by: Optional[str] = "ngay_tao",
    sort_order: Optional[str] = "desc",
    db: Session = Depends(get_db)
):
    """Lấy danh sách sản phẩm (public)."""
    query = db.query(SanPham).options(joinedload(SanPham.anh_san_phams), joinedload(SanPham.danh_muc))

    query = query.filter(SanPham.dang_hoat_dong == True)
    if search:
        query = query.filter(
            (SanPham.ten.ilike(f"%{search}%")) |
            (SanPham.mo_ta.ilike(f"%{search}%"))
        )
    if id_danh_muc:
        query = query.filter(SanPham.id_danh_muc == id_danh_muc)
    if min_price is not None:
        query = query.filter(SanPham.gia >= min_price)
    if max_price is not None:
        query = query.filter(SanPham.gia <= max_price)
    if la_noi_bat is not None:
        query = query.filter(SanPham.la_noi_bat == la_noi_bat)

    sort_column = getattr(SanPham, sort_by, SanPham.ngay_tao)
    if sort_order == "asc":
        query = query.order_by(sort_column.asc())
    else:
        query = query.order_by(sort_column.desc())

    total = query.count()
    tong_so_trang = math.ceil(total / page_size) if total > 0 else 1
    san_phams = query.offset((page - 1) * page_size).limit(page_size).all()

    items = [_build_san_pham_response(sp, db) for sp in san_phams]

    return PhanHoiDanhSachSanPham(
        items=items, tong=total, trang=page,
        kich_thuoc_trang=page_size, tong_so_trang=tong_so_trang
    )


@router.get("/admin", response_model=PhanHoiDanhSachSanPham)
def get_san_phams_admin(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
    id_danh_muc: Optional[int] = None,
    dang_hoat_dong: Optional[bool] = None,
    db: Session = Depends(get_db),
    admin: SanPham = Depends(get_current_admin)
):
    """Lấy danh sách sản phẩm (admin - bao gồm inactive)."""
    query = db.query(SanPham).options(joinedload(SanPham.anh_san_phams), joinedload(SanPham.danh_muc))

    if search:
        query = query.filter(SanPham.ten.ilike(f"%{search}%"))
    if id_danh_muc:
        query = query.filter(SanPham.id_danh_muc == id_danh_muc)
    if dang_hoat_dong is not None:
        query = query.filter(SanPham.dang_hoat_dong == dang_hoat_dong)

    query = query.order_by(SanPham.ngay_tao.desc())
    total = query.count()
    tong_so_trang = math.ceil(total / page_size) if total > 0 else 1
    san_phams = query.offset((page - 1) * page_size).limit(page_size).all()

    items = [_build_san_pham_response(sp, db) for sp in san_phams]

    return PhanHoiDanhSachSanPham(
        items=items, tong=total, trang=page,
        kich_thuoc_trang=page_size, tong_so_trang=tong_so_trang
    )


@router.get("/{san_pham_id}", response_model=PhanHoiSanPham)
def get_san_pham(san_pham_id: int, db: Session = Depends(get_db)):
    """Lấy chi tiết sản phẩm."""
    san_pham = db.query(SanPham).options(
        joinedload(SanPham.anh_san_phams), joinedload(SanPham.danh_muc)
    ).filter(SanPham.id == san_pham_id).first()

    if not san_pham:
        raise HTTPException(status_code=404, detail="Sản phẩm không tồn tại")
    return _build_san_pham_response(san_pham, db)


@router.post("", response_model=PhanHoiSanPham)
def create_san_pham(
    data: SanPhamTao,
    db: Session = Depends(get_db),
    admin: SanPham = Depends(get_current_admin)
):
    """Thêm sản phẩm mới (admin)."""
    slug = generate_slug(data.ten)
    existing = db.query(SanPham).filter(SanPham.slug == slug).first()
    if existing:
        slug = f"{slug}-{db.query(SanPham).count() + 1}"

    san_pham = SanPham(
        ten=data.ten, slug=slug,
        mo_ta=data.mo_ta, mo_ta_ngan=data.mo_ta_ngan,
        gia=data.gia, gia_khuyen_mai=data.gia_khuyen_mai,
        so_luong_ton=data.so_luong_ton, ma_sku=data.ma_sku,
        id_danh_muc=data.id_danh_muc, thuong_hieu=data.thuong_hieu,
        dang_hoat_dong=data.dang_hoat_dong, la_noi_bat=data.la_noi_bat,
        cac_kich_thuoc=data.cac_kich_thuoc
    )
    db.add(san_pham)
    db.flush()

    if data.anh_san_phams:
        for i, img in enumerate(data.anh_san_phams):
            anh = AnhSanPham(
                id_san_pham=san_pham.id,
                du_lieu_anh=img.du_lieu_anh,
                la_anh_chinh=img.la_anh_chinh or (i == 0),
                thu_tu_sap_xep=img.thu_tu_sap_xep or i
            )
            db.add(anh)

    db.commit()
    db.refresh(san_pham)

    # Ghi nhật ký
    log_activity(db, "CREATE", f"Đã thêm sản phẩm mới: {san_pham.ten}", admin.id)

    return _build_san_pham_response(san_pham, db)


@router.put("/{san_pham_id}", response_model=PhanHoiSanPham)
def update_san_pham(
    san_pham_id: int,
    data: SanPhamCapNhat,
    db: Session = Depends(get_db),
    admin: SanPham = Depends(get_current_admin)
):
    """Cập nhật sản phẩm (admin)."""
    san_pham = db.query(SanPham).filter(SanPham.id == san_pham_id).first()
    if not san_pham:
        raise HTTPException(status_code=404, detail="Sản phẩm không tồn tại")

    update_data = data.model_dump(exclude_unset=True)
    if "ten" in update_data:
        san_pham.slug = generate_slug(update_data["ten"])
    for key, value in update_data.items():
        setattr(san_pham, key, value)

    db.commit()
    db.refresh(san_pham)
    return _build_san_pham_response(san_pham, db)


@router.delete("/{san_pham_id}")
def delete_san_pham(
    san_pham_id: int,
    db: Session = Depends(get_db),
    admin: SanPham = Depends(get_current_admin)
):
    """Xóa sản phẩm (admin)."""
    san_pham = db.query(SanPham).filter(SanPham.id == san_pham_id).first()
    if not san_pham:
        raise HTTPException(status_code=404, detail="Sản phẩm không tồn tại")
    ten_sp = san_pham.ten
    db.delete(san_pham)
    db.commit()

    # Ghi nhật ký
    log_activity(db, "DELETE", f"Đã xóa sản phẩm: {ten_sp}", admin.id)

    return {"message": "Đã xóa sản phẩm"}


@router.post("/{san_pham_id}/images", response_model=AnhSanPhamBase)
def add_san_pham_image(
    san_pham_id: int,
    image: AnhSanPhamBase,
    db: Session = Depends(get_db),
    admin: SanPham = Depends(get_current_admin)
):
    """Thêm ảnh cho sản phẩm (admin)."""
    san_pham = db.query(SanPham).filter(SanPham.id == san_pham_id).first()
    if not san_pham:
        raise HTTPException(status_code=404, detail="Sản phẩm không tồn tại")

    anh = AnhSanPham(
        id_san_pham=san_pham_id,
        du_lieu_anh=image.du_lieu_anh,
        la_anh_chinh=image.la_anh_chinh,
        thu_tu_sap_xep=image.thu_tu_sap_xep
    )
    db.add(anh)
    db.commit()
    db.refresh(anh)
    return anh


@router.delete("/images/{image_id}")
def delete_san_pham_image(
    image_id: int,
    db: Session = Depends(get_db),
    admin: SanPham = Depends(get_current_admin)
):
    """Xóa ảnh sản phẩm (admin)."""
    anh = db.query(AnhSanPham).filter(AnhSanPham.id == image_id).first()
    if not anh:
        raise HTTPException(status_code=404, detail="Ảnh không tồn tại")
    db.delete(anh)
    db.commit()
    return {"message": "Đã xóa ảnh"}
