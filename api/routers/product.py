from api.cruds.inventory import add_to_inventory
from api.utils import serialize
from api.cruds.product import create_product, get_product_by_id, get_product_by_title, update_product_by_id, delete_product_by_id
from api.schemas.product import ProductSchema
from fastapi import APIRouter, status
from starlette.responses import JSONResponse
import logging
logging.basicConfig(level=logging.INFO)


router = APIRouter(tags=['Product'], prefix='/product')


@router.post('/')
async def create(product: ProductSchema):
    create = await create_product(product)
    if create:
        update_inventory = await add_to_inventory(create)
        if update_inventory and create:
            inventory = serialize.inventory(update_inventory)
            return JSONResponse(status_code=status.HTTP_200_OK, content=inventory)
    
@router.get('/{id}')
async def get_product_by_id(id: str):
    product_data = await get_product_by_id(id)
    if product_data is not None:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=product_data)
    else:
        return JSONResponse(status_code=status.HTTP_404, 
            content= {'message': 'Este produto não existe no Banco.'})
        

@router.get('/title/{title}')
async def get_product_by_title(title: str):
    product_data = await get_product_by_title(title)
    if product_data is not None:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=product_data)
    else:
        return JSONResponse(status_code=status.HTTP_404,
        content= {'message': 'Este produto não existe no Banco.'})
    
    
 # FALTA FAZER   
@router.put('/{id}')
async def update_product_by_id(id: str, product: ProductSchema):
    product_data = await update_product_by_id(id, product)
    if product_data:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=product_data)
    return {'message': 'Este produto não existe no Banco.'}
    
    
@router.delete('/{id}')
async def delete_product_by_id(id: str):
    product_data = await delete_product_by_id(id)
    if product_data is not None:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=product_data)
    else:
        return JSONResponse(status_code=status.HTTP_404,
        content= {'message': 'Este produto não existe no Banco.'})