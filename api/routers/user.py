
from api.server.database import db
from pydantic import EmailStr
from api.utils import serialize
from fastapi import APIRouter, status
from api.cruds.user import create_user, get_user_by_email, get_users
from starlette.responses import JSONResponse
from api.schemas.user import UserSchema

router = APIRouter(tags=['User'], prefix='/user')


@router.post('/')
async def create(user: UserSchema):
    user_data = await get_user_by_email(user.email)
    if user_data:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT, 
            content={'message': 'Este email já está cadastrado no sistema.'})

    create = await create_user(user)
    if create:
        user = serialize.user(create)
        return JSONResponse(status_code=status.HTTP_200_OK, content=user)

@router.get('/')
async def all():
    users = await get_users()
    if users:
        return JSONResponse(status_code=status.HTTP_200_OK, content=users)
    

@router.get("/{email}")
async def get_user_by_email(email: EmailStr, user: UserSchema):
    if email in db.user_db:
        return db.user_db[email]
    return JSONResponse(status_code=status.HTTP_200_OK, content=user)


@router.delete("/{email}")
async def delete_user(email: EmailStr, user: UserSchema):
    if email in db.user_db:
        db.user_db.pop(user)
        return JSONResponse(status_code=status.HTTP_200_OK, content=user)
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST)