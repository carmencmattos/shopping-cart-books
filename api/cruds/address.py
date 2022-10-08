from api.schemas.address import AddressSchema
from api.server.database import db
from fastapi import HTTPException, status
from bson.objectid import ObjectId
import logging
from api.utils import serialize
from pydantic.networks import EmailStr

logger = logging.getLogger(__name__)

# Consultar um endereço pelo id do usuário.
async def get_address_by_user_id(id: str):
    try:
        data = await db.address_db.find_one({'_id': ObjectId(id)})
        if data:
            return data
    except Exception as e:
        print(f'get_address.error: {e}')

# Cadastrar um endereço para um usuário.  
async def create_address(address: AddressSchema):
    try:
        await set_delivery(address.user_email)
        create_data = await db.address_db.insert_one(address.dict())
        if create_data.inserted_id:
            created = await get_address_by_user_id(create_data.inserted_id)
            return created
    except Exception as e:
        logger.exception(f'Error: {e}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        
# Consultar um endereço pelo e-mail do usuário.
async def get_address_by_id(id: str):
    try:
        data = await db.address_db.find_one({'_id': ObjectId(id)})
        if data:
            return data
    except Exception as e:
        logger.exception(f'Error: {e}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

# Consultar endereço pelo id.
async def get_address_by_id(id: str):
    address = await db.address_db.find_one({ '_id': ObjectId(id) })
    if address: 
        return address

# Consultar endereços.
async def get_addresses(email: EmailStr):
    try: 
        data = []
        async for addresses in db.address_db.find({ 'user_email': email }):
            data.append(serialize.address(addresses))
        return data
    except Exception as e:
        logger.exception(f'Error: {e}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

# Deletar endereço.
async def delete_address(address_id):
    try:
        address = await db.address_db.delete_one(
            {'_id': address_id}
        )
        if address.deleted_count:
            return {'status': 'address deleted'}
    except Exception as e:
        logger.exception(f'Error: {e}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

# Reseta todos os campos delivery para false por email do usuario
async def set_delivery(email: EmailStr):
    setDelivevry = await db.address_db.update_many({ 'user_email': email }, { '$set': { 'delivery': False } })
    if setDelivevry.modified_count:
        return True

async def set_principal_address(id: str, user_email: EmailStr):
    try:
        await set_delivery(user_email)
        update = await db.address_db.update_one({ '_id': ObjectId(id) }, { '$set': { 'delivery': True } })
        if update.modified_count:
            address = await get_address_by_id(id)
            return address
    except Exception as e:
        logger.exception(f'Error: {e}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)