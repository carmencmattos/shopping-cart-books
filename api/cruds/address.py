import email
from api.schemas.address import AddressSchema
from api.server.database import db
from fastapi import HTTPException, status
from bson.objectid import ObjectId
import logging
from pydantic.networks import EmailStr
from api.utils import serialize

logger = logging.getLogger(__name__)

# Consultar um endereço pelo id do usuário.
async def get_address_by_user_id(user_id: str):
    try:
        data = await db.address_db.find_one({'user._id': user_id})
        if data:
            return data
    except Exception as e:
        print(f'get_address.error: {e}')
        
# Cadastrar um endereço para um usuário.  
async def create_address(address: AddressSchema):
    try:
        address = await db.address_db.insert_one(address.dict())

        if address.inserted_id:
            address = await get_address_by_user_id(address.inserted_id)
            return address
    except Exception as e:
        logger.exception(f'Error: {e}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    
# Adicionar um novo endereço para um usuário.
async def insert_new_address(address_id, new_object_address):
    try:
        address = await db.address_db.update_one(
            {"_id": address_id},
            {
                '$addToSet': {
                    'address': new_object_address
                }
            }
        )
        if address.modified_count:
            # Função para buscar endereço e retornar
            address = await get_address_by_email(db.address_db, email)
            return address

    except Exception as e:
        logger.exception(f'Error: {e}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        
# Consultar um endereço pelo e-mail do usuário.
async def get_address_by_email(email):
    try:
        data = await db.address_db.find({'email': email})
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
async def get_adresses(skip, limit):  #Paginação
    try:
        address_cursor = db.address_db.find().skip(int(skip)).limit(int(limit))
        adresses = await address_cursor.to_list(length=int(limit))
        return adresses

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
