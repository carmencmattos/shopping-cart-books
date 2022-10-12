from pydantic import BaseSettings
from os import environ

class Config(BaseSettings):
    APP_NAME: str = 'Luiza Cart'
    APP_HOST: str = environ.get("APP_HOST")
    DB_HOST: str = environ.get("DB_HOST")
    SECRET: str = environ.get("TOKEN_SECRET")
    JWT_SECRET_KEY: str = environ.get("JWT_SECRET_KEY")
    JWT_ALGORITHM: str = environ.get("JWT_ALGORITHM")
    JWT_EXPIRES_IN_MIN: int = environ.get("JWT_EXPIRES_IN_MIN")

config = Config()