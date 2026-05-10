# Routers package
from app.routers.auth import router as auth_router
from app.routers.users import router as users_router
from app.routers.products import router as products_router
from app.routers.categories import router as categories_router
from app.routers.orders import router as orders_router
from app.routers.cart import router as cart_router
from app.routers.wishlists import router as wishlists_router
from app.routers.reviews import router as reviews_router
from app.routers.coupons import router as coupons_router
from app.routers.payments import router as payments_router
from app.routers.dashboard import router as dashboard_router
from app.routers.logs import router as logs_router
from app.routers.banks import router as banks_router
from app.routers.payment_methods import router as payment_methods_router
from app.routers.addresses import router as addresses_router

# Re-export for main.py
auth = auth_router
users = users_router
products = products_router
categories = categories_router
orders = orders_router
cart = cart_router
wishlists = wishlists_router
reviews = reviews_router
coupons = coupons_router
payments = payments_router
dashboard = dashboard_router
logs = logs_router
banks = banks_router
payment_methods = payment_methods_router
addresses = addresses_router
