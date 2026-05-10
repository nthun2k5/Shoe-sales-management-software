from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func as sql_func
from datetime import datetime, timedelta, timezone

from app.configs.database import get_db
from app.models import NguoiDung, SanPham, DonHang, ChiTietDonHang, DanhGia, DanhSachYeuThich
from app.utils.security import get_current_admin, get_current_user

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])


@router.get("/admin")
def admin_dashboard(db: Session = Depends(get_db), admin: NguoiDung = Depends(get_current_admin)):
    now = datetime.now(timezone.utc)
    month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    tong_nguoi_dung = db.query(NguoiDung).filter(NguoiDung.vai_tro == "khach").count()
    tong_san_pham = db.query(SanPham).count()
    san_pham_hoat_dong = db.query(SanPham).filter(SanPham.dang_hoat_dong == True).count()
    het_hang = db.query(SanPham).filter(SanPham.so_luong_ton <= 0).count()

    tong_don_hang = db.query(DonHang).count()
    don_cho_xu_ly = db.query(DonHang).filter(DonHang.trang_thai == "cho_xu_ly").count()
    don_thang_nay = db.query(DonHang).filter(DonHang.ngay_tao >= month_start).count()

    tong_doanh_thu = db.query(sql_func.sum(DonHang.thanh_tien)).filter(DonHang.trang_thai == "da_giao").scalar() or 0
    doanh_thu_thang = db.query(sql_func.sum(DonHang.thanh_tien)).filter(
        DonHang.trang_thai == "da_giao", DonHang.ngay_tao >= month_start
    ).scalar() or 0

    # Doanh thu 7 ngày gần nhất
    bieu_do_doanh_thu = []
    for i in range(6, -1, -1):
        day = (now - timedelta(days=i)).date()
        day_start = datetime.combine(day, datetime.min.time()).replace(tzinfo=timezone.utc)
        day_end = day_start + timedelta(days=1)
        rev = db.query(sql_func.sum(DonHang.thanh_tien)).filter(
            DonHang.trang_thai == "da_giao", DonHang.ngay_tao >= day_start, DonHang.ngay_tao < day_end
        ).scalar() or 0
        bieu_do_doanh_thu.append({"date": str(day), "doanh_thu": float(rev)})

    # Phân bố trạng thái đơn hàng
    phan_bo_trang_thai = {}
    for s in ["cho_xu_ly", "da_xac_nhan", "dang_giao", "da_giao", "da_huy"]:
        phan_bo_trang_thai[s] = db.query(DonHang).filter(DonHang.trang_thai == s).count()

    # Sản phẩm bán chạy
    top_san_phams = db.query(
        ChiTietDonHang.id_san_pham, sql_func.sum(ChiTietDonHang.so_luong).label("tong_da_ban")
    ).group_by(ChiTietDonHang.id_san_pham).order_by(sql_func.sum(ChiTietDonHang.so_luong).desc()).limit(5).all()

    top_list = []
    for tp in top_san_phams:
        sp = db.query(SanPham).filter(SanPham.id == tp.id_san_pham).first()
        if sp:
            top_list.append({"id": sp.id, "ten": sp.ten, "tong_da_ban": tp.tong_da_ban, "gia": sp.gia})

    # Đơn hàng gần đây
    don_hang_gan_day = db.query(DonHang).order_by(DonHang.ngay_tao.desc()).limit(5).all()
    recent_list = []
    for dh in don_hang_gan_day:
        recent_list.append({
            "id": dh.id, "ma_don_hang": dh.ma_don_hang,
            "ho_ten": dh.nguoi_dung.ho_ten if dh.nguoi_dung else "",
            "thanh_tien": dh.thanh_tien, "trang_thai": dh.trang_thai,
            "ngay_tao": str(dh.ngay_tao)
        })

    return {
        "tong_nguoi_dung": tong_nguoi_dung, "tong_san_pham": tong_san_pham,
        "san_pham_hoat_dong": san_pham_hoat_dong, "het_hang": het_hang,
        "tong_don_hang": tong_don_hang, "don_cho_xu_ly": don_cho_xu_ly,
        "don_thang_nay": don_thang_nay,
        "tong_doanh_thu": float(tong_doanh_thu), "doanh_thu_thang": float(doanh_thu_thang),
        "bieu_do_doanh_thu": bieu_do_doanh_thu, "phan_bo_trang_thai": phan_bo_trang_thai,
        "top_san_phams": top_list, "don_hang_gan_day": recent_list
    }


@router.get("/client")
def client_dashboard(db: Session = Depends(get_db), current_user: NguoiDung = Depends(get_current_user)):
    tong_don = db.query(DonHang).filter(DonHang.id_nguoi_dung == current_user.id).count()
    cho_xu_ly = db.query(DonHang).filter(DonHang.id_nguoi_dung == current_user.id, DonHang.trang_thai == "cho_xu_ly").count()
    da_giao = db.query(DonHang).filter(DonHang.id_nguoi_dung == current_user.id, DonHang.trang_thai == "da_giao").count()
    tong_chi_tieu = db.query(sql_func.sum(DonHang.thanh_tien)).filter(
        DonHang.id_nguoi_dung == current_user.id, DonHang.trang_thai == "da_giao"
    ).scalar() or 0

    don_gan_day = db.query(DonHang).filter(DonHang.id_nguoi_dung == current_user.id).order_by(DonHang.ngay_tao.desc()).limit(5).all()
    recent_list = [{"id": dh.id, "ma_don_hang": dh.ma_don_hang, "thanh_tien": dh.thanh_tien, "trang_thai": dh.trang_thai, "ngay_tao": str(dh.ngay_tao)} for dh in don_gan_day]

    so_yeu_thich = db.query(DanhSachYeuThich).filter(DanhSachYeuThich.id_nguoi_dung == current_user.id).count()

    return {
        "tong_don_hang": tong_don, "don_cho_xu_ly": cho_xu_ly,
        "don_da_giao": da_giao, "tong_chi_tieu": float(tong_chi_tieu),
        "so_yeu_thich": so_yeu_thich, "don_hang_gan_day": recent_list
    }
