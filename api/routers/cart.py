from fastapi import APIRouter, status
from pydantic.networks import EmailStr
from api.cruds.cart import add_to_set, create_cart, get_cart_by_email, insert_product, update_to_set
from api.cruds.inventory import get_inventory_by_isbn
from api.schemas.cart import CartListSchema
from api.utils import serialize
from starlette.responses import JSONResponse

router = APIRouter(tags=['Cart'], prefix='/cart')

@router.post('/{email}/create')
async def create(email: EmailStr, cart_list: CartListSchema):
    new_cart = await create_cart({ email, cart_list })
    if new_cart:
        cart = serialize.cart(new_cart)
        return JSONResponse(status_code=status.HTTP_200_OK, content=cart)

@router.post('/{email}/additem')
async def additem(email: EmailStr, item: CartListSchema ):
    inventory = await get_inventory_by_isbn(item.isbn)
    if item.quantity <= inventory['inventory']:
        has_cart = await get_cart_by_email(email)
        have = ''
        if has_cart:
            for i in has_cart['product']:
                if i['isbn'] == item.isbn:
                    have = i
            if have:
                update = await update_to_set(item.dict())
            else:
                update = await add_to_set(email, item.dict())

            # products = has_cart['product'] + [item.dict()]
            


            # cart = await insert_product(email, products)
        else:
            create = await create_cart(email, item)