from app.controllers.address import create_address, delete_address, get_address_by_id, get_addresses, set_principal_address
from app.controllers.user import get_user_by_email
from pydantic.networks import EmailStr
from fastapi import APIRouter, status
from starlette.responses import JSONResponse
from app.schemas.address import AddressSchema
from app.utils import serialize

router = APIRouter(tags=['Address'], prefix='/address')

# Busca todos os enderecos vinculados a um email
@router.get("/{email}")
async def get_address_by_email(email: EmailStr):
    addresses = await get_addresses(email)
    if addresses:
        return JSONResponse(status_code=status.HTTP_200_OK, content=addresses)

# Adiciona um novo endereco a um usuario
@router.post("/")
async def create(address: AddressSchema):
    user_data = await get_user_by_email(address.user_email)
    if user_data:
        user_address = await create_address(address)
        if user_address:
            address = serialize.address(user_address)
            return JSONResponse(status_code=status.HTTP_200_OK, content=address)
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND)

# Deleta um endereco de um usuario por id do endereco
@router.delete("/{id_address}")
async def delete(id_address: str):
    deleted = await delete_address(id_address)
    if deleted:
        return JSONResponse(status_code=status.HTTP_200_OK, content=deleted)
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST)

# Seleciona o endere;o de entrega
@router.patch("/delivery/{id}")
async def set_principal(id: str):
    address = await get_address_by_id(id)
    if (address):
        setDelivery = await set_principal_address(id, address['user_email'])
        if setDelivery:
            delivery = serialize.address(setDelivery)
            return JSONResponse(status_code=status.HTTP_200_OK, content=delivery)
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND)