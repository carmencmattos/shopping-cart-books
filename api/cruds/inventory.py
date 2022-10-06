from api.schemas.inventory import InventorySchema
from api.schemas.product import ProductSchema
from api.server.database import db
from fastapi import HTTPException, status
from bson.objectid import ObjectId
import logging
from operator import itemgetter

logger = logging.getLogger(__name__)

async def add_to_inventory(product: ProductSchema):
    try:
        inventory = await get_inventory(product.isbn)
        if inventory:
            update = await update_quantity(product)
            return update
        else:
            inventory_data = { 'product': product.dict(), 'inventory': product.quantity }
                
            create = await create_inventory(inventory_data)
            return create
    except Exception as e:
        logger.exception(f'Error: {e}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

async def get_inventory(isbn: str):
    inventory = await db.inventory_db.find_one({'product.isbn': isbn})
    if inventory:
        return inventory

async def update_quantity(product: ProductSchema):
    inventory = await db.inventory_db.find_one({ 'product.isbn': product.isbn })
    if inventory:
        updated_quantity = inventory['inventory'] + product.quantity
        updated = await db.inventory_db.update_one({ 'product.isbn': product.isbn }, { '$set': { 'inventory': updated_quantity} })
        if updated.modified_count:
            new_inventory = await get_inventory_by_isbn(product.isbn)
            return new_inventory
        


async def create_inventory(inventory: InventorySchema):
    new = await db.inventory_db.insert_one(inventory)
    if new.inserted_id:
        new_inventory = await get_inventory_by_id(new.inserted_id)
        return new_inventory

async def get_inventory_by_id(id: str):
    inventory = await db.inventory_db.find_one({'_id': ObjectId(id)})
    if inventory:
        return inventory

async def get_inventory_by_isbn(isbn: str):
    inventory = await db.inventory_db.find_one({'product.isbn': isbn})
    if inventory:
        return inventory