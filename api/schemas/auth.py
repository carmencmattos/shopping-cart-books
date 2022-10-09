from pydantic import BaseModel
from pydantic.networks import EmailStr


class LoginData(BaseModel):
    email: EmailStr
    password: str
