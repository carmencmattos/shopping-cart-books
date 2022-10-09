from pydantic import BaseModel
from pydantic.networks import EmailStr

from api.schemas.user import UserSchema


class LoginData(BaseModel):
    email: EmailStr
    password: str


class SignUpSchema(BaseModel):
    CPF: int
    name: str
    phone_number: int
    email: EmailStr
    password: str
