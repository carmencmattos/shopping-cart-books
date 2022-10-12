from app.controllers.inventory import add_to_inventory
from app.utils import serialize
from app.controllers.product import create_product, get_product_by_id, get_product_by_title, update_product_by_isbn, get_all_products
from app.schemas.product import ProductSchema, ProductUpdateSchema
from fastapi import APIRouter, status
from starlette.responses import JSONResponse
import logging
logging.basicConfig(level=logging.INFO)

router = APIRouter(tags=['Product'], prefix='/product')

# Cadastrar um produto


@router.post('/')
async def create(product: ProductSchema):
    create = await create_product(product.dict())
    if create:
        update_inventory = await add_to_inventory(create)
        if update_inventory and create:
            product = serialize.product(create)
            inventory = serialize.inventory(update_inventory)
            return JSONResponse(status_code=status.HTTP_200_OK, content={'product': product, 'invevntory': inventory})

# Pesquisar um produto pelo ID do MongoDB


@router.get('/{id}')
async def get_by_id(id: str):
    product_data = await get_product_by_id(id)
    if product_data is not None:
        product = serialize.product(product_data)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=product)
    else:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                            content={'message': 'Este produto não existe no Banco.'})


@router.get('/')
async def all():
    users = await get_all_products()
    if users:
        return JSONResponse(status_code=status.HTTP_200_OK, content=users)

# Pesquisar um produto pelo nome (titulo)


@router.get('/title/{title}')
async def get_by_title(title: str):
    product_data = await get_product_by_title(title)
    if product_data is not None:
        product = serialize.product(product_data)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=product)
    else:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                            content={'message': 'Este produto não existe no Banco.'})

# Atualizar os dados do produto pelo codigo


@router.patch('/{isbn}')
async def update(isbn: str, product_fields: ProductUpdateSchema):
    product_data = await update_product_by_isbn(isbn, product_fields.dict())
    if product_data:
        product = serialize.product(product_data)
        return JSONResponse(status_code=status.HTTP_200_OK, content=product)
