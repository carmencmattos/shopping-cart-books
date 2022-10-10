from api.schemas.auth import LoginData, SignUpSchema
from api.utils import serialize
from fastapi import APIRouter, status
from api.cruds.user import create_user, get_user_by_email
from starlette.responses import JSONResponse
from api.schemas.user import UserSchema
from api.providers import hash_provider, token_provider

router = APIRouter(tags=['Auth'], prefix='/auth')


# Criar um novo user na aplicação
@router.post('/signup')
async def signup(sign_up_data: SignUpSchema):
    email = sign_up_data.email
    user_data = await get_user_by_email(email)
    if user_data:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={'message': 'Este email já está cadastrado no sistema.'})
    sign_up_data.password = hash_provider.create_hash(sign_up_data.password)
    user = UserSchema(CPF=sign_up_data.CPF, name=sign_up_data.name,
                      phone_number=sign_up_data.phone_number, email=sign_up_data.email, password=sign_up_data.password)
    create = await create_user(user)
    if create:
        user = serialize.user(create)
        return JSONResponse(status_code=status.HTTP_200_OK, content=user)


# Login com email e senha e retorna as infos do usuário e o token de acesso
@router.post('/login')
async def signup(login_data: LoginData):
    email = login_data.email
    password = login_data.password
    user_data = await get_user_by_email(email)
    if not user_data:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={'message': 'Email ou Senha estão incorretos.'})

    valid_password = hash_provider.verify_hash(
        password, user_data['password'])

    if not valid_password:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={'message': 'Email ou Senha estão incorretos.'})

    token = token_provider.create_access_token({'sub': user_data['email']})

    user = serialize.user(user_data)
    return JSONResponse(status_code=status.HTTP_200_OK, content={'user': user, 'access_token': token})
