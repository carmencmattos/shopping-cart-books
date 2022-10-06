from api.schemas.product import ProductSchema
from api.server.database import db
from fastapi import HTTPException, status
from bson.objectid import ObjectId
import logging

logger = logging.getLogger(__name__)

async def create_product(product: ProductSchema):
    try:
        ups_product = await db.product_db.replace_one({"isbn": product.isbn}, product.dict(), upsert=True)

        if ups_product.upserted_id:
            new_product = await get_product_by_id(ups_product.upserted_id)
            return new_product
        else:
            return product
    except Exception as e:
        logger.exception(f'Error: {e}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

async def get_product_by_id(id: str):
    product = await db.product_db.find_one({ '_id': ObjectId(id) })
    if product: 
        return product

async def get_product_by_title(title: str):
    product = await db.product_db.find_one({ 'title': title })
    if product: 
        return product
    
async def update_product_by_id(id: str, product: ProductSchema):
    await db.product_db.update_product_by_id({ 'id': ObjectId(id), 'product': product }) 
    return product

async def delete_product_by_id(id: str):
    await db.product_db.delete_product_by_id({ '_id': ObjectId(id) })