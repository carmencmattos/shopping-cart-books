from fastapi import HTTPException, status
from app.controllers.inventory import remove_quantity_from_inventory
from app.server.database import db
from app.schemas.cart import CartListSchema, CartSchema
from bson.objectid import ObjectId
import logging
from pydantic.networks import EmailStr
from datetime import datetime
from app.controllers.product import get_product_by_isbn
from app.controllers.order import get_order_by_id

logger = logging.getLogger(__name__)

async def create_cart_by_email(email: EmailStr):
    try:
        cart = dict(user_email= email, product=[], open=True, created_at=datetime.now(), updated_at=datetime.now())
        create = await db.cart_db.insert_one(cart)
        if create.inserted_id:
            cart = await get_cart_by_id(create.inserted_id)
            logger.info(f'Carrinho criado para o usuario: {email}')
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

async def get_closed_cart_by_email(email: EmailStr):
    cart_closed = await db.order_db.find_one({ 'user_email': email, 'open': False })
    if cart_closed:
        return cart_closed

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
        remove_item = await db.cart_db.update_one({ 'user_email': email, 'open': True }, { '$pull': { 'product': { 'isbn': isbn } } })
        if remove_item.modified_count:
            return True
    except Exception as e:
        logger.exception(f'Error: {e}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

async def drop_cart_by_email(email: EmailStr):
    try:
        remove_item = await db.cart_db.delete_one({ 'user_email': email, 'open': True })
        if remove_item.deleted_count:
            return True
    except Exception as e:
        logger.exception(f'Error: {e}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

async def calculate_cart(data_cart):
    try:
        product_info = []
        for products in data_cart['product']:
            data = await get_product_by_isbn(products['isbn'])
            del data['quantity']
            data['quantity'] = products['quantity']
            product_info.append(data)  

        del data_cart['product']
        data_cart['product'] = product_info

        total_info = []
        for prd_info in data_cart['product']:
            calc = prd_info['quantity'] * prd_info['price']
            total_per_product_info = dict(isbn=prd_info['isbn'], quantity=prd_info['quantity'], price=prd_info['price'], total_price=calc)
            total_info.append(total_per_product_info)

        total_cart = { 'total': 0 }
        for final_info in total_info:
            total_cart['total'] += final_info['total_price']

        response = { 'data_cart': data_cart, 'total_info': total_info, 'total': total_cart }
        return response
    except Exception as e:
        logger.exception(f'Error: {e}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

async def delete_cart_by_email(cart: CartSchema):
    try:
        del cart['open']
        cart['open'] = False
        to_order = await db.order_db.insert_one(cart)
        if to_order.inserted_id:
            delete = await db.cart_db.delete_one({ '_id': ObjectId(cart['_id']) })
            if delete.deleted_count:
                order = await get_order_by_id(to_order.inserted_id)
                if order:
                    for products in cart['product']:
                        await remove_quantity_from_inventory(products['isbn'], products['quantity'])
                    return order
    except Exception as e:
        logger.exception(f'Error: {e}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)  
