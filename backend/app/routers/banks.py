from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app.configs.database import get_db
from app.models.bank import ThongTinNganHang
from app.schemas.bank import NganHangTao, NganHangCapNhat, NganHangPhanHoi
from app.utils.security import get_current_admin


router = APIRouter(prefix="/api/banks", tags=["Banks"])


@router.get("/active", response_model=List[NganHangPhanHoi])
def get_active_banks(
    loai: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Lấy danh sách ngân hàng/ví đang sử dụng (Dành cho Client)."""
    query = db.query(ThongTinNganHang).filter(ThongTinNganHang.dang_su_dung == True)
    if loai:
        query = query.filter(ThongTinNganHang.loai == loai)
    return query.all()


@router.get("", response_model=List[NganHangPhanHoi])
def get_all_banks(
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    """Lấy tất cả ngân hàng/ví (Admin)."""
    return db.query(ThongTinNganHang).all()


@router.post("", response_model=NganHangPhanHoi)
def create_bank(
    data: NganHangTao,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    """Thêm tài khoản ngân hàng/ví mới (Admin)."""
    bank = ThongTinNganHang(**data.model_dump())
    db.add(bank)
    db.commit()
    db.refresh(bank)
    return bank


@router.put("/{bank_id}", response_model=NganHangPhanHoi)
def update_bank(
    bank_id: int,
    data: NganHangCapNhat,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    """Cập nhật tài khoản ngân hàng/ví (Admin)."""
    bank = db.query(ThongTinNganHang).filter(ThongTinNganHang.id == bank_id).first()
    if not bank:
        raise HTTPException(status_code=404, detail="Không tìm thấy tài khoản")
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(bank, key, value)
    db.commit()
    db.refresh(bank)
    return bank


@router.delete("/{bank_id}")
def delete_bank(
    bank_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    """Xóa tài khoản ngân hàng/ví (Admin)."""
    bank = db.query(ThongTinNganHang).filter(ThongTinNganHang.id == bank_id).first()
    if not bank:
        raise HTTPException(status_code=404, detail="Không tìm thấy tài khoản")
    db.delete(bank)
    db.commit()
    return {"message": "Đã xóa tài khoản"}
