from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.configs.database import get_db
from app.models.payment_method import PhuongThucThanhToan
from app.schemas.payment_method import (
    TaoPhuongThucThanhToan, CapNhatPhuongThucThanhToan, PhanHoiPhuongThucThanhToan
)
from app.utils.security import get_current_user, get_current_admin as require_admin

router = APIRouter(prefix="/api/payment-methods", tags=["payment-methods"])


@router.get("/active", response_model=List[PhanHoiPhuongThucThanhToan])
def lay_phuong_thuc_kich_hoat(db: Session = Depends(get_db)):
    """Lấy danh sách phương thức thanh toán đang kích hoạt (dành cho client)"""
    return db.query(PhuongThucThanhToan).filter(
        PhuongThucThanhToan.kich_hoat == True
    ).order_by(PhuongThucThanhToan.thu_tu.asc()).all()


@router.get("/", response_model=List[PhanHoiPhuongThucThanhToan])
def lay_tat_ca(db: Session = Depends(get_db), current_user=Depends(require_admin)):
    """Lấy tất cả phương thức thanh toán (admin)"""
    return db.query(PhuongThucThanhToan).order_by(PhuongThucThanhToan.thu_tu.asc()).all()


@router.post("/", response_model=PhanHoiPhuongThucThanhToan)
def tao_phuong_thuc(
    data: TaoPhuongThucThanhToan,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    existing = db.query(PhuongThucThanhToan).filter(
        PhuongThucThanhToan.ma_phuong_thuc == data.ma_phuong_thuc
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Mã phương thức đã tồn tại")
    phuong_thuc = PhuongThucThanhToan(**data.model_dump())
    db.add(phuong_thuc)
    db.commit()
    db.refresh(phuong_thuc)
    return phuong_thuc


@router.put("/{id}", response_model=PhanHoiPhuongThucThanhToan)
def cap_nhat_phuong_thuc(
    id: int,
    data: CapNhatPhuongThucThanhToan,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    phuong_thuc = db.query(PhuongThucThanhToan).filter(PhuongThucThanhToan.id == id).first()
    if not phuong_thuc:
        raise HTTPException(status_code=404, detail="Không tìm thấy phương thức thanh toán")
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(phuong_thuc, field, value)
    db.commit()
    db.refresh(phuong_thuc)
    return phuong_thuc


@router.delete("/{id}")
def xoa_phuong_thuc(
    id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    phuong_thuc = db.query(PhuongThucThanhToan).filter(PhuongThucThanhToan.id == id).first()
    if not phuong_thuc:
        raise HTTPException(status_code=404, detail="Không tìm thấy phương thức thanh toán")
    db.delete(phuong_thuc)
    db.commit()
    return {"message": "Đã xóa phương thức thanh toán"}
