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
    user = await db.user_db.find_one({ '_id': ObjectId(id) })
    if user: 
        return user

# Consultar um usuário pelo pelo seu email.
async def get_user_by_email(email: EmailStr):
    user = await db.user_db.find_one({ 'email': email })
    if user: 
        return user

# Consultar usuários.
async def get_users():
    data = []
    async for user in db.user_db.find():
        data.append(serialize.user(user))
    return data

# Deletar usuário.
async def delete_user(user_id):
    try:
        user = await db.users_db.delete_one(
            {'_id': user_id}
        )
        if user.deleted_count:
            return {'status': 'User deleted'} 
    except Exception as e:
        logger.exception(f'Error: {e}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)