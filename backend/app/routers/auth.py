from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.configs.database import get_db
from app.models import NguoiDung
from app.schemas import NguoiDungDangKy, NguoiDungDangNhap, PhanHoiToken, YeCauRefreshToken
from app.utils.security import (
    hash_password, verify_password,
    create_access_token, create_refresh_token, decode_token
)
from app.utils.logger import log_activity

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/register", response_model=PhanHoiToken)
def register(data: NguoiDungDangKy, db: Session = Depends(get_db)):
    """Đăng ký tài khoản mới."""
    existing = db.query(NguoiDung).filter(NguoiDung.email == data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email đã được sử dụng")

    nguoi_dung = NguoiDung(
        email=data.email,
        mat_khau_hash=hash_password(data.mat_khau),
        ho_ten=data.ho_ten,
        so_dien_thoai=data.so_dien_thoai,
        vai_tro="khach"
    )
    db.add(nguoi_dung)
    db.commit()
    db.refresh(nguoi_dung)

    access_token = create_access_token(data={"sub": str(nguoi_dung.id)})
    refresh_token = create_refresh_token(data={"sub": str(nguoi_dung.id)})

    return PhanHoiToken(
        access_token=access_token,
        refresh_token=refresh_token,
        nguoi_dung={
            "id": nguoi_dung.id, "email": nguoi_dung.email, "ho_ten": nguoi_dung.ho_ten,
            "so_dien_thoai": nguoi_dung.so_dien_thoai, "vai_tro": nguoi_dung.vai_tro,
            "dang_hoat_dong": nguoi_dung.dang_hoat_dong
        }
    )


@router.post("/login", response_model=PhanHoiToken)
def login(data: NguoiDungDangNhap, db: Session = Depends(get_db)):
    """Đăng nhập."""
    nguoi_dung = db.query(NguoiDung).filter(NguoiDung.email == data.email).first()
    if not nguoi_dung or not verify_password(data.mat_khau, nguoi_dung.mat_khau_hash):
        raise HTTPException(status_code=401, detail="Email hoặc mật khẩu không đúng")
    if not nguoi_dung.dang_hoat_dong:
        raise HTTPException(status_code=403, detail="Tài khoản đã bị khóa")

    access_token = create_access_token(data={"sub": str(nguoi_dung.id)})
    refresh_token = create_refresh_token(data={"sub": str(nguoi_dung.id)})

    # Ghi nhật ký đăng nhập
    log_activity(db, "LOGIN", f"Người dùng {nguoi_dung.email} đã đăng nhập", nguoi_dung.id)

    return PhanHoiToken(
        access_token=access_token,
        refresh_token=refresh_token,
        nguoi_dung={
            "id": nguoi_dung.id, "email": nguoi_dung.email, "ho_ten": nguoi_dung.ho_ten,
            "so_dien_thoai": nguoi_dung.so_dien_thoai, "vai_tro": nguoi_dung.vai_tro,
            "dang_hoat_dong": nguoi_dung.dang_hoat_dong,
            "anh_dai_dien": nguoi_dung.anh_dai_dien, "dia_chi": nguoi_dung.dia_chi
        }
    )


@router.post("/refresh", response_model=PhanHoiToken)
def refresh_token(data: YeCauRefreshToken, db: Session = Depends(get_db)):
    """Làm mới access token."""
    payload = decode_token(data.refresh_token)
    if payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Token không hợp lệ")

    sub = payload.get("sub")
    try:
        nguoi_dung_id = int(sub)
    except (ValueError, TypeError):
        raise HTTPException(status_code=401, detail="Token không hợp lệ")
        
    nguoi_dung = db.query(NguoiDung).filter(NguoiDung.id == nguoi_dung_id).first()
    if not nguoi_dung or not nguoi_dung.dang_hoat_dong:
        raise HTTPException(status_code=401, detail="Người dùng không tồn tại hoặc đã bị khóa")

    access_token = create_access_token(data={"sub": str(nguoi_dung.id)})
    new_refresh_token = create_refresh_token(data={"sub": str(nguoi_dung.id)})

    return PhanHoiToken(
        access_token=access_token,
        refresh_token=new_refresh_token,
        nguoi_dung={
            "id": nguoi_dung.id, "email": nguoi_dung.email, "ho_ten": nguoi_dung.ho_ten,
            "so_dien_thoai": nguoi_dung.so_dien_thoai, "vai_tro": nguoi_dung.vai_tro,
            "dang_hoat_dong": nguoi_dung.dang_hoat_dong,
            "anh_dai_dien": nguoi_dung.anh_dai_dien, "dia_chi": nguoi_dung.dia_chi
        }
    )
