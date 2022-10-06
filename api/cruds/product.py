from api.schemas.product import ProductSchema
from api.server.database import db
from fastapi import HTTPException, status
from bson.objectid import ObjectId
import logging

logger = logging.getLogger(__name__)

async def create_product(product: ProductSchema):
    try:
        new_product = await db['product'].insert_one(product)
        created_product = await db['product'].find_one({'_id': new_product.inserted_id})
        raise HTTPException(status_code=status.HTTP_201_CREATED, content=created_product)
    except Exception as e:
        logger.exception(f'Error: {e}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

async def get_product_by_id(id: str):
  
    if (product := await  db['product'].find_one({ '_id': ObjectId(id)})) is not None:
        return product
    raise HTTPException(status_code=404, detail=f"Product {id} not found")
  

async def get_product_by_title(title: str):
    if (product := await db['product'].find_one({ 'title': title })) is not None:
        return product
    raise HTTPException(status_code=404, detail=f"Product {id} not found")
    
async def update_product_by_id(id: str, product: ProductSchema):
    #tem que fazer as regras do update
    update_product = await  db['product'].update_one({ '_id':  ObjectId(id), 'product': product }) 
    return update_product

async def delete_product_by_id(id: str):
    delete_product = await db['product'].delete_one({ '_id': ObjectId(id) })
    if  delete_product.deleted_count == 1:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Product {id} deleted") 