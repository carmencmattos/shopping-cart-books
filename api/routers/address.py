from api.server.database import db
from pydantic import EmailStr
from fastapi import APIRouter, status
from starlette.responses import JSONResponse
from api.schemas.address import AddressSchema

router = APIRouter(tags=['Address'], prefix='/address')

@router.get("/{email}/address/")
async def get_address_by_email(email: EmailStr):
    address = []
    if email not in db.user_db:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST)
    for email in db.address_db:
        if db.address_db[email].email == email:
            address.append(db.user_db[email])
    return address

@router.post("/address/")
async def create_address(address: AddressSchema):
    if address.email not in db.user_db:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST)
    if address.id in db.address_db:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT, 
            content={'message': 'Este endereço já está cadastrado.'})
    id_new_address = len(list(db.address_db)) + 1
    address.id = id_new_address
    db.address_db[id_new_address] = address
    return JSONResponse(status_code=status.HTTP_200_OK, content=address)


@router.delete("/{id_address}")
async def delete_address(id_address: int):
    if id in db.user_db:
        return id[id].address.pop(id_address)
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST)

@router.get('/')
async def teste():
    return 'teste'