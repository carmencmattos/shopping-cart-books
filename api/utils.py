from api.schemas.inventory import InventorySchema
from api.schemas.address import AddressSchema
from api.schemas.product import ProductSchema
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
        address['_id'] = str(address['created_at'])
        address['_id'] = str(address['updated_at'])
        return address


    def product(product: ProductSchema):
        product['_id'] = str(product['_id'])
        product['created_at'] = str(product['created_at'])
        product['updated_at'] = str(product['updated_at'])
        return product
        
    def inventory(inventory: InventorySchema):
        inventory['_id'] = str(inventory['_id'])
        inventory['product']['updated_at'] = str(inventory['product']['updated_at'])
        inventory['product']['created_at'] = str(inventory['product']['created_at'])
        return inventory