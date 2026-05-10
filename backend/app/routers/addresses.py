from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.configs.database import get_db
from app.models.address import DiaChiGiaoHang
from app.schemas.address import DiaChiTao, DiaChiCapNhat, DiaChiPhanHoi
from app.utils.security import get_current_user
from app.models.user import NguoiDung

router = APIRouter(prefix="/api/addresses", tags=["Addresses"])


@router.get("", response_model=List[DiaChiPhanHoi])
def get_user_addresses(
    db: Session = Depends(get_db),
    current_user: NguoiDung = Depends(get_current_user)
):
    """Lấy danh sách địa chỉ của người dùng."""
    return db.query(DiaChiGiaoHang).filter(DiaChiGiaoHang.id_nguoi_dung == current_user.id).all()


@router.post("", response_model=DiaChiPhanHoi)
def create_address(
    data: DiaChiTao,
    db: Session = Depends(get_db),
    current_user: NguoiDung = Depends(get_current_user)
):
    """Thêm địa chỉ mới."""
    # Nếu đặt làm mặc định, bỏ mặc định các địa chỉ khác
    if data.la_mac_dinh:
        db.query(DiaChiGiaoHang).filter(
            DiaChiGiaoHang.id_nguoi_dung == current_user.id
        ).update({"la_mac_dinh": False})

    address = DiaChiGiaoHang(**data.model_dump(), id_nguoi_dung=current_user.id)
    db.add(address)
    db.commit()
    db.refresh(address)
    return address


@router.put("/{address_id}", response_model=DiaChiPhanHoi)
def update_address(
    address_id: int,
    data: DiaChiCapNhat,
    db: Session = Depends(get_db),
    current_user: NguoiDung = Depends(get_current_user)
):
    """Cập nhật địa chỉ."""
    address = db.query(DiaChiGiaoHang).filter(
        DiaChiGiaoHang.id == address_id,
        DiaChiGiaoHang.id_nguoi_dung == current_user.id
    ).first()

    if not address:
        raise HTTPException(status_code=404, detail="Không tìm thấy địa chỉ")

    update_data = data.model_dump(exclude_unset=True)
    
    if update_data.get("la_mac_dinh"):
        db.query(DiaChiGiaoHang).filter(
            DiaChiGiaoHang.id_nguoi_dung == current_user.id
        ).update({"la_mac_dinh": False})

    for key, value in update_data.items():
        setattr(address, key, value)

    db.commit()
    db.refresh(address)
    return address


@router.delete("/{address_id}")
def delete_address(
    address_id: int,
    db: Session = Depends(get_db),
    current_user: NguoiDung = Depends(get_current_user)
):
    """Xóa địa chỉ."""
    address = db.query(DiaChiGiaoHang).filter(
        DiaChiGiaoHang.id == address_id,
        DiaChiGiaoHang.id_nguoi_dung == current_user.id
    ).first()

    if not address:
        raise HTTPException(status_code=404, detail="Không tìm thấy địa chỉ")

    db.delete(address)
    db.commit()
    return {"message": "Đã xóa địa chỉ"}


@router.post("/{address_id}/set-default", response_model=DiaChiPhanHoi)
def set_default_address(
    address_id: int,
    db: Session = Depends(get_db),
    current_user: NguoiDung = Depends(get_current_user)
):
    """Đặt địa chỉ làm mặc định."""
    db.query(DiaChiGiaoHang).filter(
        DiaChiGiaoHang.id_nguoi_dung == current_user.id
    ).update({"la_mac_dinh": False})

    address = db.query(DiaChiGiaoHang).filter(
        DiaChiGiaoHang.id == address_id,
        DiaChiGiaoHang.id_nguoi_dung == current_user.id
    ).first()

    if not address:
        raise HTTPException(status_code=404, detail="Không tìm thấy địa chỉ")

    address.la_mac_dinh = True
    db.commit()
    db.refresh(address)
    return address
