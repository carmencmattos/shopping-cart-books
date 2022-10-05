from fastapi import APIRouter
from api.routers import user
from api.routers import product
from api.routers import cart

routers = APIRouter()

routers.include_router(user.router)
routers.include_router(product.router)
routers.include_router(cart.router)