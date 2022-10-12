from typing import List
from pydantic import BaseModel, Field
from pydantic.networks import EmailStr
from datetime import datetime

class AddressSchema(BaseModel):
    user_email: EmailStr
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