from datetime import datetime
from pydantic import BaseModel, Field
from pydantic.networks import EmailStr
from datetime import datetime
from typing import List

class CartListSchema(BaseModel):
    isbn: str
    quantity: int = Field(default=0)

class CartSchema(BaseModel):
    user_email: EmailStr
    open: bool = Field(default=True)
    product: List[CartListSchema] = []
    created_at: datetime = Field(datetime.now())
    updated_at: datetime = Field(datetime.now())

