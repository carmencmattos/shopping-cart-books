from fastapi import APIRouter, status
from app.controllers.auth import get_admin
from app.controllers.user import deactivate_user_by_id, get_user_by_email, get_users, get_users_disabled, activate_user_by_id
from starlette.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import status, Depends
from starlette.responses import JSONResponse
from pydantic.networks import EmailStr
from app.utils import serialize

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

# Ativar usuario por email
@router.patch("/activate/{email}", dependencies=[Depends(get_admin)])
async def activate_user(email: EmailStr):
    user = await get_user_by_email(email)
    if user:
        activate = await activate_user_by_id(user['_id'])
        if activate:
            return JSONResponse(status_code=status.HTTP_200_OK, content={'message': 'Usuário ativado com sucesso'})
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={'message': 'Usuário não encontrado'})