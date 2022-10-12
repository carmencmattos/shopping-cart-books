from pydantic.networks import EmailStr
from api.utils import serialize
from fastapi import APIRouter, status
from api.cruds.user import create_user, deactivate_user_by_id, get_user_by_email, get_users
from starlette.responses import JSONResponse
from api.schemas.user import UserSchema
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(tags=['User'], prefix='/user')
oauth_form = OAuth2PasswordRequestForm

# Cadastrar cliente
@router.post('/')
async def create(user: UserSchema):
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

# Pesquisar cliente por email
@router.get("/{email}")
async def get_user_email(email: EmailStr):
    user_data = await get_user_by_email(email)
    if user_data:
        user = serialize.user(user_data)
        return JSONResponse(status_code=status.HTTP_200_OK, content=user)

