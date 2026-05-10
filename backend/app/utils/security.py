from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import JWTError, jwt
import bcrypt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.configs.config import settings
from app.configs.database import get_db
from app.models import NguoiDung

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())
    except Exception:
        return False


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=settings.JWT_TOKEN_EXPIRE))
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, settings.JWT_KEY, algorithm=settings.ALGORITHM)


def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=7)
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, settings.JWT_KEY, algorithm=settings.ALGORITHM)


def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.JWT_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token không hợp lệ hoặc đã hết hạn",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> NguoiDung:
    payload = decode_token(token)
    sub = payload.get("sub")
    if sub is None:
        raise HTTPException(status_code=401, detail="Token không hợp lệ")
    try:
        nguoi_dung_id = int(sub)
    except (ValueError, TypeError):
        raise HTTPException(status_code=401, detail="Token không hợp lệ")

    nguoi_dung = db.query(NguoiDung).filter(NguoiDung.id == nguoi_dung_id).first()
    if nguoi_dung is None:
        raise HTTPException(status_code=401, detail="Người dùng không tồn tại")
    if not nguoi_dung.dang_hoat_dong:
        raise HTTPException(status_code=403, detail="Tài khoản đã bị khóa")
    return nguoi_dung


async def get_current_admin(current_user: NguoiDung = Depends(get_current_user)) -> NguoiDung:
    if current_user.vai_tro != "quan_tri":
        raise HTTPException(status_code=403, detail="Bạn không có quyền truy cập")
    return current_user
