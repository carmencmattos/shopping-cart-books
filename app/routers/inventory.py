
from app.controllers.inventory import update_inventory_by_isbn
from app.schemas.inventory import InventoryUpdateSchema
from app.server.database import db
from app.utils import serialize
from fastapi import APIRouter, status
from starlette.responses import JSONResponse

router = APIRouter(tags=['Inventory'], prefix='/inventory')

# Atualizar quantidade em estoque por ISBN
@router.patch('/{isbn}')
async def update(isbn: str, inventory_fields: InventoryUpdateSchema):
    inventory_data = await update_inventory_by_isbn(isbn, inventory_fields.dict())
    if inventory_data:
        inventory = serialize.inventory(inventory_data)
        return JSONResponse(status_code=status.HTTP_200_OK, content=inventory)
    