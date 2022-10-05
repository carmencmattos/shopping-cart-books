from datetime import datetime
from pydantic import BaseModel, Field
from datetime import datetime

class ProductSchema(BaseModel):
    title: str
    author: str
    publishing_company: str
    year: int
    gener: str
    description: str
    ISBN: str
    language: str
    pages: int
    price: float = Field(gt = 0.01)
    inventory: int = Field(gt = 0)
    created_at: datetime = Field(datetime.now())
    updated_at: datetime = Field(datetime.now())