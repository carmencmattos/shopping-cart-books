from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
import logging
from api.config import config
import jwt
from api.server.database import db
from bson.objectid import ObjectId
from pydantic.networks import EmailStr
from passlib.context import CryptContext


logger = logging.getLogger(__name__)
oauth2 = OAuth2PasswordBearer(tokenUrl='token')
bcrypt = CryptContext(schemes=['bcrypt'])

async def authentication(email: EmailStr, password: str):
    try:
        user = await db.user_db.find_one({ 'email': email, 'active': True })
        if user:
            verified = bcrypt.verify(password, user['password'])
            if verified:
                return user
    except Exception as e:
        logger.exception(f'Error: {e}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

async def get_user_auth(token: str = Depends(oauth2)):
    try:
        payload = jwt.decode(token, config.SECRET, algorithms=['HS256'])
        user = await db.user_db.find_one({ '_id': ObjectId(payload.get('id')) })
        if user:
            return user
    except Exception as e:
        logger.exception(f'Error: {e}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    

async def get_admin(token: str = Depends(oauth2)):
    try:
        user = await get_user_auth(token)
        if not user['admin'] or not user['active']:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Incorrect e-mail or password')   
        return user
    except Exception as e:
        logger.exception(f'Error: {e}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
