from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from app.configs.database import get_db
from app.models.log import NhatKy as LogModel
from app.schemas.log import NhatKy as LogSchema
from app.utils.security import get_current_admin, get_current_user
from app.models.user import NguoiDung
from app.models.order import DonHang

router = APIRouter(
    prefix="/api/logs",
    tags=["logs"]
)


@router.get("/", response_model=List[LogSchema])
def get_logs(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: NguoiDung = Depends(get_current_admin)
):
    """
    Lấy danh sách nhật ký hoạt động (Dành cho Admin)
    """
    logs = (
        db.query(LogModel)
        .options(joinedload(LogModel.nguoi_dung))
        .order_by(LogModel.ngay_tao.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    result = []
    for log in logs:
        log_data = LogSchema.model_validate(log)
        log_data.ten_nguoi_dung = log.nguoi_dung.ho_ten if log.nguoi_dung else "Hệ thống"
        result.append(log_data)
    return result


@router.get("/order/{order_id}", response_model=List[LogSchema])
def get_order_logs(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: Optional[NguoiDung] = Depends(get_current_user)
):
    """
    Lấy lịch sử tác động của một đơn hàng.
    Người dùng chỉ xem được lịch sử đơn hàng của chính mình.
    Admin xem được tất cả.
    """
    don_hang = db.query(DonHang).filter(DonHang.id == order_id).first()
    if not don_hang:
        raise HTTPException(status_code=404, detail="Đơn hàng không tồn tại")
    if current_user.vai_tro != "quan_tri" and don_hang.id_nguoi_dung != current_user.id:
        raise HTTPException(status_code=403, detail="Không có quyền truy cập")
    logs = (
        db.query(LogModel)
        .options(joinedload(LogModel.nguoi_dung))
        .filter(LogModel.id_don_hang == order_id)
        .order_by(LogModel.ngay_tao.asc())
        .all()
    )
    result = []
    for log in logs:
        log_data = LogSchema.model_validate(log)
        log_data.ten_nguoi_dung = log.nguoi_dung.ho_ten if log.nguoi_dung else "Hệ thống"
        result.append(log_data)
    return result
