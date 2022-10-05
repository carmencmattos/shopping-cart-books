from datetime import datetime
from pydantic import BaseModel, Field
from pydantic.networks import EmailStr
from datetime import datetime

from api.schemas.user import UserSchema
from typing import List
class CartListSchema(BaseModel):
    product: ProductSchema
    qt_product: int 
class CartSchema(BaseModel):
    client: UserSchema
    open: bool = Field(default=True)
    product: List[CartListSchema] = []
    active: bool = Field(default=True)
    created_at: datetime = Field(datetime.now())
    updated_at: datetime = Field(datetime.now())

