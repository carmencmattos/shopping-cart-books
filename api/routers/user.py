from api.routers.auth_utils import get_user_logged
from api.server.database import db
from pydantic.networks import EmailStr
from api.utils import serialize
from fastapi import APIRouter, Depends, HTTPException, status
from api.controllers.user import create_user, deactivate_user_by_id, get_user_by_email, get_users
from starlette.responses import JSONResponse
from api.schemas.user import UserSchema

router = APIRouter(tags=['User'], prefix='/user')

# Cadastrar cliente


@router.post('/')
async def create(user: UserSchema, authenticated_user: UserSchema = Depends(get_user_logged)):
    if authenticated_user['admin']:
        email = user.email
        user_data = await get_user_by_email(email)
        if user_data:
            return JSONResponse(
                status_code=status.HTTP_409_CONFLICT,
                content={'message': 'Este email já está cadastrado no sistema.'})

        create = await create_user(user)
        if create:
            user = serialize.user(create)
            return JSONResponse(status_code=status.HTTP_200_OK, content=user)
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail='Forbidden')


# Retorna todos os clientes cadastrados


@router.get('/')
async def all():
    users = await get_users()
    if users:
        return JSONResponse(status_code=status.HTTP_200_OK, content=users)


# Autentica o usuário através do token passado na requisição e retornar as informações do usuário


@router.get('/me')
def me(authenticated_user: UserSchema = Depends(get_user_logged)):
    user = serialize.user(authenticated_user)
    return user

# Pesquisar cliente por email


@router.get("/{email}")
async def get_user_email(email: EmailStr):
    user_data = await get_user_by_email(email)
    if user_data:
        user = serialize.user(user_data)
        return JSONResponse(status_code=status.HTTP_200_OK, content=user)

# Desativar usuario por email


@router.patch("/deactivate/{email}")
async def delete_user(email: EmailStr):
    user = await get_user_by_email(email)
    if user:
        deactivate = await deactivate_user_by_id(user['_id'])
        if deactivate:
            user = serialize.user(deactivate)
            return JSONResponse(status_code=status.HTTP_200_OK, content=user)
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST)
