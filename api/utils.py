from .schemas.user import UserSchema

class serialize:
    def user(user: UserSchema):
        user['_id'] = str(user['_id'])
        user['created_at'] = str(user['created_at'])
        user['updated_at'] = str(user['updated_at'])
        del user['password']
        return user