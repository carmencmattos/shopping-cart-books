from fastapi import HTTPException, status
from api.server.database import db
from api.schemas.cart import CartListSchema
from bson.objectid import ObjectId
import logging
from pydantic.networks import EmailStr
from datetime import datetime

logger = logging.getLogger(__name__)

async def create_cart(email: EmailStr, products: CartListSchema):
    try:
        cart = dict(user_email= email, product=[products.dict()], open=True, created_at=datetime.now(), updated_at=datetime.now())
        create = await db.cart_db.insert_one(cart)
        if create.inserted_id:
            cart = await get_cart_by_id(create.inserted_id)
            return cart
    except Exception as e:
        logger.exception(f'Error: {e}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

async def get_cart_by_id(id: str):
    cart_opened = await db.cart_db.find_one({ '_id': ObjectId(id), 'open': True })
    if cart_opened:
        return cart_opened

async def get_cart_by_email(email: EmailStr):
    cart_opened = await db.cart_db.find_one({ 'user_email': email, 'open': True })
    if cart_opened:
        return cart_opened

async def insert_product(email: EmailStr, products: CartListSchema):
    try:
        cart = await db.cart_db.update_one({ 'product.isbn': email }, { '$set': { 'product': products } })
    except Exception as e:
        logger.exception(f'Error: {e}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

async def update_product_cart(products, has_cart):
    try:
        remove_item = await remove_item_from_cart(has_cart['user_email'], products['isbn'])
        if remove_item:
            add_product_cart = await db.cart_db.update_one({ 'user_email': has_cart['user_email'] }, { '$addToSet': { 'product': products } })
            if add_product_cart.matched_count:
                cart_updated = await get_cart_by_email(has_cart['user_email'])
                if cart_updated:
                    return cart_updated
    except Exception as e:
        logger.exception(f'Error: {e}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

async def add_product_cart(email: EmailStr, products):
    try:
        add_product_cart = await db.cart_db.update_one({ 'user_email': email }, { '$addToSet': { 'product': products } })
        if add_product_cart.matched_count:
            cart_updated = await get_cart_by_email(email)
            if cart_updated:
                return cart_updated
    except Exception as e:
        logger.exception(f'Error: {e}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

async def remove_item_from_cart(email: EmailStr, isbn: str):
    try:
        remove_item = await db.cart_db.update_one({ 'user_email': email }, { '$pull': { 'product': { 'isbn': isbn } } })
        if remove_item.modified_count:
            return True
    except Exception as e:
        logger.exception(f'Error: {e}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)