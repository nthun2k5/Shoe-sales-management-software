from sqlalchemy.orm import Session
from app.models.log import NhatKy
from typing import Optional


def log_activity(
    db: Session,
    hanh_dong: str,
    mo_ta: Optional[str] = None,
    nguoi_dung_id: Optional[int] = None,
    ip_address: Optional[str] = None,
    id_don_hang: Optional[int] = None
):
    """
    Ghi lại nhật ký hoạt động vào cơ sở dữ liệu.
    """
    try:
        new_log = NhatKy(
            nguoi_dung_id=nguoi_dung_id,
            hanh_dong=hanh_dong,
            mo_ta=mo_ta,
            ip_address=ip_address,
            id_don_hang=id_don_hang
        )
        db.add(new_log)
        db.commit()
        db.refresh(new_log)
        return new_log
    except Exception as e:
        print(f"Lỗi khi ghi nhật ký: {e}")
        db.rollback()
        return None
