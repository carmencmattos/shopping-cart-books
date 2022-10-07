from pydantic import BaseModel

class InventorySchema(BaseModel):
    isbn: str
    inventory: int

class InventoryUpdateSchema(BaseModel):
    inventory: int