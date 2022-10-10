from jose import jwt
from datetime import datetime, timedelta
from api.config import config


def create_access_token(data: dict):
    data_copy = data.copy()
    expiration = datetime.utcnow() + timedelta(minutes=config.JWT_EXPIRES_IN_MIN)
    data_copy.update({'exp': expiration})
    token_jwt = jwt.encode(data_copy, config.JWT_SECRET_KEY,
                           algorithm=config.JWT_ALGORITHM)
    return token_jwt


def verify_access_token(token: str):
    payload = jwt.decode(token, config.JWT_SECRET_KEY,
                         algorithms=[config.JWT_ALGORITHM])
    return payload.get('sub')
