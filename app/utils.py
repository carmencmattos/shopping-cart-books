from app.schemas.cart import CartSchema
from app.schemas.inventory import InventorySchema
from app.schemas.address import AddressSchema
from app.schemas.product import ProductSchema
from .schemas.user import UserSchema
from .schemas.product import ProductSchema
class serialize:
    def user(user: UserSchema):
        user['_id'] = str(user['_id'])
        user['created_at'] = str(user['created_at'])
        user['updated_at'] = str(user['updated_at'])
        del user['password']
        return user

    def address(address: AddressSchema):
        address['_id'] = str(address['_id'])
        address['created_at'] = str(address['created_at'])
        address['updated_at'] = str(address['updated_at'])
        return address


    def product(product: ProductSchema):
        product['_id'] = str(product['_id'])
        product['created_at'] = str(product['created_at'])
        product['updated_at'] = str(product['updated_at'])
        return product
        
    def inventory(inventory: InventorySchema):
        inventory['_id'] = str(inventory['_id'])
        return inventory

    def cart(cart: CartSchema):
        cart['_id'] = str(cart['_id'])
        cart['created_at'] = str(cart['created_at'])
        cart['updated_at'] = str(cart['updated_at'])
        for data in cart['product']:
            data['_id'] = str(data['_id'])
            del data['created_at']
            del data['updated_at']
        return cart

    def get_cart(cart):
        cart['_id'] = str(cart['_id'])
        cart['created_at'] = str(cart['created_at'])
        cart['updated_at'] = str(cart['updated_at'])
        return cart