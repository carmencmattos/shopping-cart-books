from app.schemas.product import ProductSchema, ProductUpdateSchema
from app.server.database import db
from fastapi import HTTPException, status
from bson.objectid import ObjectId
import logging

logger = logging.getLogger(__name__)

async def create_product(product: ProductSchema):
    try:
        ups_product = await db.product_db.replace_one({ 'isbn': product['isbn'] }, product, upsert=True)
        if ups_product.upserted_id:
            new_product = await get_product_by_id(ups_product.upserted_id)
            if new_product:
                return new_product
        else:
            product_data = await get_product_by_isbn(product['isbn'])
            if product_data:
                return product_data
    except Exception as e:
        logger.exception(f'Error: {e}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

# Pesquisar produto pelo codigo informado
async def get_product_by_isbn(isbn: str):
    product = await db.product_db.find_one({ 'isbn': isbn })
    if product:
        return product

# Pesquisar produto pelo ID do MongoDB
async def get_product_by_id(id: str):
    product = await db.product_db.find_one({ '_id': ObjectId(id)})
    if product:
        return product
  
# Pesquisar produto pelo nome
async def get_product_by_title(title: str):
    product = await db.product_db.find_one({ 'title': title })
    if product:
        return product
    
# Atualizar produto pelo codigo
async def update_product_by_isbn(isbn: str, product_fields: ProductUpdateSchema):
    update_product = await  db.product_db.update_one({ 'isbn': isbn }, { '$set': product_fields })
    if update_product.matched_count:
        product = await get_product_by_isbn(isbn)
        if product:
            return product

async def delete_product_by_id(id: str):
    delete_product = await db['product'].delete_one({ '_id': ObjectId(id) })
    if  delete_product.deleted_count == 1:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Product {id} deleted") 