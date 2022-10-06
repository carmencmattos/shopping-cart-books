from datetime import datetime
from pydantic import BaseModel, Field
from datetime import datetime

from api.schemas.product import ProductSchema

class InventorySchema(BaseModel):
    product: ProductSchema
    inventory: int