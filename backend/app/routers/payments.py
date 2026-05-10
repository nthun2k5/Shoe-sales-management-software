from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.configs.database import get_db
from app.models import ThanhToan, DonHang, NguoiDung
from app.schemas import PhanHoiThanhToan, XacNhanThanhToan
from app.utils.security import get_current_admin

router = APIRouter(prefix="/api/payments", tags=["Payments"])


@router.get("/{thanh_toan_id}", response_model=PhanHoiThanhToan)
def get_thanh_toan(thanh_toan_id: int, db: Session = Depends(get_db), admin: NguoiDung = Depends(get_current_admin)):
    thanh_toan = db.query(ThanhToan).filter(ThanhToan.id == thanh_toan_id).first()
    if not thanh_toan:
        raise HTTPException(status_code=404, detail="Không tìm thấy")
    return thanh_toan


@router.put("/{thanh_toan_id}/confirm", response_model=PhanHoiThanhToan)
def confirm_thanh_toan(thanh_toan_id: int, data: XacNhanThanhToan, db: Session = Depends(get_db), admin: NguoiDung = Depends(get_current_admin)):
    thanh_toan = db.query(ThanhToan).filter(ThanhToan.id == thanh_toan_id).first()
    if not thanh_toan:
        raise HTTPException(status_code=404, detail="Không tìm thấy")
    thanh_toan.trang_thai = "da_hoan_thanh"
    thanh_toan.thoi_diem_thanh_toan = datetime.now(timezone.utc)
    if data.ma_giao_dich:
        thanh_toan.ma_giao_dich = data.ma_giao_dich
    don_hang = db.query(DonHang).filter(DonHang.id == thanh_toan.id_don_hang).first()
    if don_hang:
        don_hang.trang_thai_thanh_toan = "da_thanh_toan"
    db.commit()
    db.refresh(thanh_toan)
    return thanh_toan
