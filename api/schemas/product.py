from datetime import datetime
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