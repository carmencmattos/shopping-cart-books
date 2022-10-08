from api.cruds.address import create_address
from api.schemas.user import UserSchema
from api.server.database import db
from fastapi import HTTPException, status
from bson.objectid import ObjectId
import logging
from pydantic.networks import EmailStr
from api.utils import serialize

logger = logging.getLogger(__name__)

# Cadastrar um usuário com um nome e um e-mail único. 
async def create_user(user: UserSchema):
    try:
        user = await db.user_db.insert_one(user.dict())

        if user.inserted_id:
            user = await get_user_by_id(user.inserted_id)
            return user
    except Exception as e:
        logger.exception(f'Error: {e}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

# Consultar um usuário pelo seu id.
async def get_user_by_id(id: str):
    user = await db.user_db.find_one({ '_id': ObjectId(id), 'active': True })
    if user: 
        return user

# Consultar um usuário pelo pelo seu email.
async def get_user_by_email(email: EmailStr):
    user = await db.user_db.find_one({ 'email': email, 'active': True })
    if user: 
        return user

# Consultar usuários.
async def get_users():
    data = []
    async for user in db.user_db.find({ 'active': True }):
        data.append(serialize.user(user))
    return data

# Desativar usuário.
async def deactivate_user_by_id(id: str):
    try:
        update = await db.user_db.update_one({ '_id': ObjectId(id) }, { '$set': { 'active': False } })
        if update.modified_count:
            user = await get_user_by_id(id)
            return user
    except Exception as e:
        logger.exception(f'Error: {e}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)    
