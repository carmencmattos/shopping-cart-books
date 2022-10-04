from typing import List
from pydantic import BaseModel, Field
from datetime import datetime
from api.schemas.user import UserSchema


class Address(BaseModel):
    id_user: int
    street: str
    number: int
    complement: str
    cep: str
    district: str
    city: str
    state: str
    delivery: bool = Field(default=True)
    created_at: datetime = Field(datetime.now())
    updated_at: datetime = Field(datetime.now())


class AddressSchema(BaseModel):
    user: UserSchema
    address: List[Address] = []