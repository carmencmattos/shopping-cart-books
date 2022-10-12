from fastapi import APIRouter
from app.routers import user
from app.routers import product
from app.routers import cart
from app.routers import inventory
from app.routers import address
from app.routers import order
from app.routers import admin
from app.routers import auth

routers = APIRouter()

routers.include_router(user.router)
routers.include_router(product.router)
routers.include_router(cart.router)
routers.include_router(inventory.router)
routers.include_router(address.router)
routers.include_router(order.router)
routers.include_router(admin.router)
routers.include_router(auth.router)