from fastapi import APIRouter
from api.routers import user
from api.routers import product
from api.routers import cart
from api.routers import inventory
from api.routers import address

routers = APIRouter()

routers.include_router(user.router)
routers.include_router(product.router)
routers.include_router(cart.router)
routers.include_router(inventory.router)
routers.include_router(address.router)