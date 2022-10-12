from fastapi import APIRouter, status
from api.cruds.auth import get_admin
from api.cruds.user import deactivate_user_by_id, get_user_by_email, get_users, get_users_disabled
from starlette.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import status, Depends
from starlette.responses import JSONResponse
from pydantic.networks import EmailStr
from api.utils import serialize

router = APIRouter(tags=['Admin'], prefix='/admin/user')
oauth_form = OAuth2PasswordRequestForm

# Retorna todos os clientes cadastrados
@router.get('/enabled', dependencies=[Depends(get_admin)])
async def all():
    users = await get_users()
    if users:
        return JSONResponse(status_code=status.HTTP_200_OK, content=users)

@router.get('/disabled', dependencies=[Depends(get_admin)])
async def all():
    users = await get_users_disabled()
    if users:
        return JSONResponse(status_code=status.HTTP_200_OK, content=users)

# Desativar usuario por email
@router.patch("/deactivate/{email}", dependencies=[Depends(get_admin)])
async def delete_user(email: EmailStr):
    user = await get_user_by_email(email)
    if user:
        deactivate = await deactivate_user_by_id(user['_id'])
        if deactivate:
            return JSONResponse(status_code=status.HTTP_200_OK, content={'message': 'Usuário desativado com sucesso'})
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={'message': 'Usuário não encontrado'})

