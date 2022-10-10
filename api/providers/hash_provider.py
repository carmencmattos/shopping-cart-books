from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'])


def verify_hash(text, text_hashed):
    return pwd_context.verify(text, text_hashed)


def create_hash(text):
    return pwd_context.hash(text)
