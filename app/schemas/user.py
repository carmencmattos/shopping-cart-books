from pydantic import BaseModel, Field
from pydantic.networks import EmailStr
from datetime import datetime

class UserSchema(BaseModel):
    cpf: int = Field(unique=True, index=True)
    name: str
    phone_number: int 
    email: EmailStr = Field(unique=True, index=True)
    password: str
    active: bool = Field(default=True)
    admin: bool = Field(default=False)
    created_at: datetime = Field(datetime.now())
    updated_at: datetime = Field(datetime.now())





    