from fastapi import APIRouter, status
from pydantic.networks import EmailStr
from starlette.responses import JSONResponse

from api.cruds.order import get_order_by_email
from api.cruds.cart import calculate_cart
from api.utils import serialize

router = APIRouter(tags=['Order'], prefix='/order')

@router.get('/{email}')
async def get_cart(email: EmailStr):
    get_cart = await get_order_by_email(email)
    if get_cart:
        cart = await calculate_cart(get_cart)
        return_object = { 'cart': serialize.cart(cart['data_cart']), 'payments': cart['total_info'], 'total_cart': cart['total'] }
        return JSONResponse(status_code=status.HTTP_200_OK, content=return_object)
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={'message': 'Email ou Order inexistentes'})