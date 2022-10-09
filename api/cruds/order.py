from api.server.database import db
from bson.objectid import ObjectId
from pydantic.networks import EmailStr

async def get_order_by_id(id: str):
    cart_opened = await db.order_db.find_one({ '_id': ObjectId(id), 'open': False })
    if cart_opened:
        return cart_opened

async def get_order_by_email(email: EmailStr):
    order = await db.order_db.find_one({ 'user_email': email, 'open': False })
    if order:
        return order