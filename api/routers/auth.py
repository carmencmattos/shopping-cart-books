from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from api.cruds.auth import authentication
from starlette.responses import JSONResponse
from api.config import config
import jwt

router = APIRouter(tags=['Auth'], prefix='/auth')
oauth_form = OAuth2PasswordRequestForm

@router.post('/login')
async def get_token(form: oauth_form = Depends()):
    auth_user = await authentication(form.username, form.password)
    if auth_user:
        payload = {
            'id': str(auth_user['_id']),
            'email': auth_user['email'],
            'active': auth_user['active'],
            'admin': auth_user['admin']
        }
        token = jwt.encode(payload, config.SECRET, algorithm='HS256')
        return JSONResponse(status_code=status.HTTP_200_OK, content={'access_token': token, 'token_type': 'bearer'})
    return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'message': 'Usuário não autorizado'})
