from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from api.controllers.user import get_user_by_email
from api.providers import token_provider

oauth2_schema = OAuth2PasswordBearer(tokenUrl='token')


async def get_user_logged(token: str = Depends(oauth2_schema)):
    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid Token')
    try:
        email = token_provider.verify_access_token(token)
    except JWTError:
        raise exception

    if not email:
        raise exception

    user = await get_user_by_email(email)
    if not user:
        raise exception

    return user
