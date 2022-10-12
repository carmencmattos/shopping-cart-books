from app.schemas.user import UserSchema
from app.server.database import db
from fastapi import HTTPException, status
from bson.objectid import ObjectId
import logging
from pydantic.networks import EmailStr
from app.utils import serialize
from passlib.context import CryptContext

logger = logging.getLogger(__name__)
bcrypt = CryptContext(schemes=['bcrypt'])


# Cadastrar um usuário com um nome e um e-mail único. 
async def create_user(user: UserSchema):
    try:
        password = bcrypt.encrypt(user.password)
        user.password = password
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

# Consultar um usuário pelo pelo seu cpf.
async def get_user_by_cpf(cpf: str):
    user = await db.user_db.find_one({ 'cpf': cpf, 'active': True })
    if user: 
        return user

# Consultar usuários Ativos.
async def get_users():
    data = []
    async for user in db.user_db.find({ 'active': True }):
        data.append(serialize.user(user))
    return data

# Consultar usuários Desativados.
async def get_users_disabled():
    data = []
    async for user in db.user_db.find({ 'active': False }):
        data.append(serialize.user(user))
    return data

# Desativar usuário.
async def deactivate_user_by_id(id: str):
    try:
        update = await db.user_db.update_one({ '_id': ObjectId(id) }, { '$set': { 'active': False } })
        if update.modified_count:
            return True
    except Exception as e:
        logger.exception(f'Error: {e}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)    
