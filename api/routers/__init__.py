from fastapi import APIRouter
from api.routers import user
from api.routers import product
from api.routers import cart
from api.routers import inventory
from api.routers import address
from api.routers import order
from api.routers import admin
from api.routers import auth

routers = APIRouter()

routers.include_router(user.router)
routers.include_router(product.router)
routers.include_router(cart.router)
routers.include_router(inventory.router)
routers.include_router(address.router)
routers.include_router(order.router)
routers.include_router(admin.router)
routers.include_router(auth.router)