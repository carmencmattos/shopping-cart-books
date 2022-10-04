from pydantic import BaseSettings
from os import environ

class Config(BaseSettings):
    APP_NAME: str = 'Luiza Cart'
    APP_HOST: str = environ.get("APP_HOST")
    DB_HOST: str = environ.get("DB_HOST")

config = Config()