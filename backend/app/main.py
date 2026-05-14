from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.configs.config import settings
from app.configs.database import engine, Base
from app.models import *  # noqa: F401, F403 - import all models to register them

from app.routers import auth, users, products, categories, orders, cart, wishlists, reviews, coupons, payments, dashboard, logs, banks, payment_methods, addresses, chatbot

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="QLBG - Quản Lý Bán Hàng API",
    description="API cho phần mềm quản lý bán hàng",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(auth)
app.include_router(users)
app.include_router(products)
app.include_router(categories)
app.include_router(orders)
app.include_router(cart)
app.include_router(wishlists)
app.include_router(reviews)
app.include_router(coupons)
app.include_router(payments)
app.include_router(dashboard)
app.include_router(logs)
app.include_router(banks)
app.include_router(payment_methods)
app.include_router(addresses)
app.include_router(chatbot.router)


@app.get("/")
def root():
    return {"message": "QLBG API đang hoạt động", "version": "1.0.0"}


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.on_event("startup")
def seed_payment_methods():
    from app.configs.database import SessionLocal
    from app.models.payment_method import PhuongThucThanhToan

    DEFAULT_METHODS = [
        {
            "ma_phuong_thuc": "cod",
            "ten_phuong_thuc": "Thanh toán COD",
            "mo_ta": "Tiền mặt khi nhận hàng",
            "icon_svg": '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M17 9V7a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2m2 4h10a2 2 0 002-2v-6a2 2 0 00-2-2H9a2 2 0 00-2 2v6a2 2 0 002 2zm7-5a2 2 0 11-4 0 2 2 0 014 0z"/></svg>',
            "kich_hoat": True,
            "ho_tro_qr": False,
            "loai": "cod",
            "thu_tu": 4,
            "phi_co_dinh": 0,
            "phi_phan_tram": 0,
            "gia_tri_don_toi_thieu": None,
            "gia_tri_don_toi_da": None,
            "cau_hinh_json": None,
            "anh_logo": None,
        },
        {
            "ma_phuong_thuc": "bank_transfer",
            "ten_phuong_thuc": "Chuyển khoản ngân hàng",
            "mo_ta": "Qua app ngân hàng / QR Code",
            "icon_svg": '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M8 14v3m4-3v3m4-3v3M3 21h18M3 10h18M3 7l9-4 9 4M4 10h16v11H4V10z"/></svg>',
            "kich_hoat": True,
            "ho_tro_qr": True,
            "loai": "bank",
            "thu_tu": 3,
            "phi_co_dinh": 0,
            "phi_phan_tram": 0,
            "gia_tri_don_toi_thieu": 10000,
            "gia_tri_don_toi_da": None,
            "cau_hinh_json": None,
            "anh_logo": None,
        },
        {
            "ma_phuong_thuc": "momo",
            "ten_phuong_thuc": "Ví MoMo",
            "mo_ta": "Thanh toán qua số điện thoại / QR",
            "icon_svg": '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z"/></svg>',
            "kich_hoat": True,
            "ho_tro_qr": True,
            "loai": "momo",
            "thu_tu": 2,
            "phi_co_dinh": 0,
            "phi_phan_tram": 1,
            "gia_tri_don_toi_thieu": 20000,
            "gia_tri_don_toi_da": 50000000,
            "cau_hinh_json": None,
            "anh_logo": None,
        },
        {
            "ma_phuong_thuc": "zalopay",
            "ten_phuong_thuc": "ZaloPay",
            "mo_ta": "Thanh toán qua số điện thoại / QR",
            "icon_svg": '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 8c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zm0 10c-4.41 0-8-1.79-8-4V6c0-2.21 3.59-4 8-4s8 1.79 8 4v8c0 2.21-3.59 4-8 4z"/></svg>',
            "kich_hoat": True,
            "ho_tro_qr": True,
            "loai": "zalopay",
            "thu_tu": 1,
            "phi_co_dinh": 1100,
            "phi_phan_tram": 0,
            "gia_tri_don_toi_thieu": 20000,
            "gia_tri_don_toi_da": 20000000,
            "cau_hinh_json": None,
            "anh_logo": None,
        },
    ]

    db = SessionLocal()
    try:
        if db.query(PhuongThucThanhToan).count() == 0:
            for m in DEFAULT_METHODS:
                db.add(PhuongThucThanhToan(**m))
            db.commit()
            print("✅ Đã seed 4 phương thức thanh toán")
    finally:
        db.close()


@app.on_event("startup")
def create_default_admin():
    from app.configs.database import SessionLocal
    from app.models import NguoiDung
    from app.utils.security import hash_password

    db = SessionLocal()
    try:
        admin = db.query(NguoiDung).filter(NguoiDung.email == "admin@qlbg.com").first()
        if not admin:
            admin = NguoiDung(
                email="admin@qlbg.com",
                mat_khau_hash=hash_password("admin123"),
                ho_ten="Quản Trị Viên",
                vai_tro="quan_tri",
                dang_hoat_dong=True
            )
            db.add(admin)
            db.commit()
            print("✅ Đã tạo tài khoản admin mặc định: admin@qlbg.com / admin123")
    finally:
        db.close()

