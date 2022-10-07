from api.schemas.inventory import InventorySchema, InventoryUpdateSchema
from api.schemas.product import ProductSchema
from api.server.database import db
from fastapi import HTTPException, status
from bson.objectid import ObjectId
import logging

logger = logging.getLogger(__name__)

async def add_to_inventory(product: ProductSchema):
    try:
        inventory = await get_inventory(product['isbn'])
        if inventory:
            update = await update_quantity(inventory, product)
            return update
        else:
            inventory_data = dict(isbn=product['isbn'], inventory=product['quantity'])
            create = await create_inventory(inventory_data)
            return create
    except Exception as e:
        logger.exception(f'Error: {e}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

async def get_inventory(isbn: str):
    inventory = await db.inventory_db.find_one({'isbn': isbn})
    if inventory:
        return inventory

async def update_quantity(inventory: InventorySchema, product: ProductSchema):
    updated_quantity = inventory['inventory'] + product['quantity']
    updated = await db.inventory_db.update_one({ 'isbn': product['isbn'] }, { '$set': { 'inventory': updated_quantity }} )
    if updated.modified_count:
        new_inventory = await get_inventory_by_isbn(product['isbn'])
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
    inventory = await db.inventory_db.find_one({ 'isbn': isbn })
    if inventory:
        return inventory

async def update_inventory_by_isbn(isbn: str, inventory_fields: InventoryUpdateSchema):
    try:
        update_inventory = await  db.inventory_db.update_one({ 'isbn': isbn }, { '$set': inventory_fields })
        if update_inventory.matched_count:
            product = await get_inventory_by_isbn(isbn)
            if product:
                return product
    except Exception as e:
        logger.exception(f'Error: {e}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)