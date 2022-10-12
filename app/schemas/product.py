from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, confloat, conint
from datetime import datetime


class ProductSchema(BaseModel):
    title: str
    author: str
    publishing_company: str
    year: int
    edition: int
    gener: str
    description: str
    isbn: str
    language: str
    pages: int
    price: confloat(gt=0.01)
    quantity: conint(gt=0)
    created_at: datetime = Field(datetime.now())
    updated_at: datetime = Field(datetime.now())


class ProductUpdateSchema(BaseModel):
    title: Optional[str]
    author: Optional[str]
    publishing_company: Optional[str]
    year: Optional[int]
    edition: Optional[int]
    gener: Optional[str]
    description: Optional[str]
    language: Optional[str]
    pages: Optional[int]
    price: Optional[confloat(gt=0.01)]
