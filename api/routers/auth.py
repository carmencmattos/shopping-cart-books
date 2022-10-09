from api.schemas.auth import LoginData
from api.utils import serialize
from fastapi import APIRouter, status
from api.cruds.user import create_user, get_user_by_email
from starlette.responses import JSONResponse
from api.schemas.user import UserSchema
from api.providers import hash_provider, token_provider

router = APIRouter(tags=['Auth'], prefix='/auth')


@router.post('/signup')
async def signup(user: UserSchema):
    email = user.email
    user_data = await get_user_by_email(email)
    if user_data:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={'message': 'Este email já está cadastrado no sistema.'})
    user.password = hash_provider.gerar_hash(user.password)
    create = await create_user(user)
    if create:
        user = serialize.user(create)
        return JSONResponse(status_code=status.HTTP_200_OK, content=user)


@router.post('/login')
async def signup(login_data: LoginData):
    email = login_data.email
    password = login_data.password
    user_data = await get_user_by_email(email)
    if not user_data:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={'message': 'Email ou Senha estão incorretos.'})

    valid_password = hash_provider.verificar_hash(
        password, user_data['password'])

    if not valid_password:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={'message': 'Email ou Senha estão incorretos.'})

    token = token_provider.criar_access_token({'sub': user_data['email']})

    user = serialize.user(user_data)
    return JSONResponse(status_code=status.HTTP_200_OK, content={'user': user, 'access_token': token})
