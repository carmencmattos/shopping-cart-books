from .schemas.user import UserSchema
from .schemas.product import ProductSchema
class serialize:
    def user(user: UserSchema):
        user['_id'] = str(user['_id'])
        user['created_at'] = str(user['created_at'])
        user['updated_at'] = str(user['updated_at'])
        del user['password']
        return user

    def product(product: ProductSchema):
        product['_id'] = str(product['_id'])
        product['created_at'] = str(product['created_at'])
        product['updated_at'] = str(product['updated_at'])
        return product
        