from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.configs.database import get_db
from app.models import NguoiDung
from app.schemas import PhanHoiNguoiDung, NguoiDungCapNhat, NguoiDungTao
from app.utils.security import get_current_user, get_current_admin, hash_password, verify_password
from app.utils.logger import log_activity

router = APIRouter(prefix="/api/users", tags=["Users"])


@router.get("", response_model=List[PhanHoiNguoiDung])
def get_users(
    skip: int = 0, limit: int = 20,
    search: str = None,
    db: Session = Depends(get_db),
    admin: NguoiDung = Depends(get_current_admin)
):
    """Lấy danh sách người dùng (admin)."""
    query = db.query(NguoiDung)
    if search:
        query = query.filter(
            (NguoiDung.ho_ten.ilike(f"%{search}%")) |
            (NguoiDung.email.ilike(f"%{search}%"))
        )
    return query.offset(skip).limit(limit).all()


@router.post("", response_model=PhanHoiNguoiDung)
def create_user(
    data: NguoiDungTao,
    db: Session = Depends(get_db),
    admin: NguoiDung = Depends(get_current_admin)
):
    """Tạo người dùng mới (admin)."""
    if db.query(NguoiDung).filter(NguoiDung.email == data.email).first():
        raise HTTPException(status_code=400, detail="Email đã được sử dụng")
    nguoi_dung = NguoiDung(
        email=data.email,
        mat_khau_hash=hash_password(data.mat_khau),
        ho_ten=data.ho_ten,
        so_dien_thoai=data.so_dien_thoai,
        dia_chi=data.dia_chi,
        vai_tro=data.vai_tro,
    )
    db.add(nguoi_dung)
    db.commit()
    db.refresh(nguoi_dung)
    log_activity(db, "USER_CREATE", f"Tạo người dùng mới {nguoi_dung.email}", admin.id, id_don_hang=None)
    return nguoi_dung


@router.get("/me", response_model=PhanHoiNguoiDung)
def get_me(current_user: NguoiDung = Depends(get_current_user)):
    """Lấy thông tin người dùng hiện tại."""
    return current_user


@router.put("/me", response_model=PhanHoiNguoiDung)
def update_me(
    data: NguoiDungCapNhat,
    db: Session = Depends(get_db),
    current_user: NguoiDung = Depends(get_current_user)
):
    """Cập nhật thông tin cá nhân."""
    if data.ho_ten is not None:
        current_user.ho_ten = data.ho_ten
    if data.so_dien_thoai is not None:
        current_user.so_dien_thoai = data.so_dien_thoai
    if data.dia_chi is not None:
        current_user.dia_chi = data.dia_chi
    db.commit()
    db.refresh(current_user)
    return current_user


@router.put("/me/password")
def change_password(
    data: NguoiDungDoiMatKhau,
    db: Session = Depends(get_db),
    current_user: NguoiDung = Depends(get_current_user)
):
    """Đổi mật khẩu."""
    if not verify_password(data.mat_khau_hien_tai, current_user.mat_khau_hash):
        raise HTTPException(status_code=400, detail="Mật khẩu hiện tại không đúng")
    current_user.mat_khau_hash = hash_password(data.mat_khau_moi)
    db.commit()
    return {"message": "Đổi mật khẩu thành công"}


@router.put("/me/avatar", response_model=PhanHoiNguoiDung)
def update_avatar(
    avatar_data: dict,
    db: Session = Depends(get_db),
    current_user: NguoiDung = Depends(get_current_user)
):
    """Upload avatar (base64)."""
    avatar_base64 = avatar_data.get("avatar")
    current_user.anh_dai_dien = avatar_base64
    db.commit()
    db.refresh(current_user)
    return current_user



@router.put("/{user_id}", response_model=PhanHoiNguoiDung)
def update_user(
    user_id: int,
    data: NguoiDungCapNhat,
    db: Session = Depends(get_db),
    admin: NguoiDung = Depends(get_current_admin)
):
    """Cập nhật thông tin người dùng (admin)."""
    nguoi_dung = db.query(NguoiDung).filter(NguoiDung.id == user_id).first()
    if not nguoi_dung:
        raise HTTPException(status_code=404, detail="Người dùng không tồn tại")
    if data.ho_ten is not None:
        nguoi_dung.ho_ten = data.ho_ten
    if data.so_dien_thoai is not None:
        nguoi_dung.so_dien_thoai = data.so_dien_thoai
    if data.dia_chi is not None:
        nguoi_dung.dia_chi = data.dia_chi
    if data.vai_tro is not None:
        nguoi_dung.vai_tro = data.vai_tro
    db.commit()
    db.refresh(nguoi_dung)
    log_activity(db, "USER_UPDATE", f"Cập nhật người dùng {nguoi_dung.email}", admin.id, id_don_hang=None)
    return nguoi_dung


@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin: NguoiDung = Depends(get_current_admin)
):
    """Xóa người dùng (admin)."""
    nguoi_dung = db.query(NguoiDung).filter(NguoiDung.id == user_id).first()
    if not nguoi_dung:
        raise HTTPException(status_code=404, detail="Người dùng không tồn tại")
    if nguoi_dung.id == admin.id:
        raise HTTPException(status_code=400, detail="Không thể xóa tài khoản của chính mình")
    email = nguoi_dung.email
    db.delete(nguoi_dung)
    db.commit()
    log_activity(db, "USER_DELETE", f"Xóa người dùng {email}", admin.id, id_don_hang=None)
    return {"message": "Đã xóa người dùng"}


@router.put("/{user_id}/toggle-active")
def toggle_user_active(
    user_id: int,
    db: Session = Depends(get_db),
    admin: NguoiDung = Depends(get_current_admin)
):
    """Khóa/Mở khóa tài khoản (admin)."""
    nguoi_dung = db.query(NguoiDung).filter(NguoiDung.id == user_id).first()
    if not nguoi_dung:
        raise HTTPException(status_code=404, detail="Người dùng không tồn tại")
    if nguoi_dung.id == admin.id:
        raise HTTPException(status_code=400, detail="Không thể khóa tài khoản của chính mình")
    nguoi_dung.dang_hoat_dong = not nguoi_dung.dang_hoat_dong
    db.commit()
    return {"message": f"Tài khoản {'đã mở khóa' if nguoi_dung.dang_hoat_dong else 'đã bị khóa'}"}
