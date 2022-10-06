from os import environ
from motor.motor_asyncio import AsyncIOMotorClient
from api.config import config
import logging
logging.basicConfig(level=logging.INFO)

db_name = 'luiza_cart'

class Database():
    client: AsyncIOMotorClient = None
    database_uri = environ.get("DATABASE_URI")
    user_db = None
    address_db = None
    product_db = None
    cart_db = None

db = Database()

async def connect():
    db.client = AsyncIOMotorClient(config.DB_HOST, maxPoolSize=10, minPoolSize=10)
    db.user_db = db.client[db_name].user
    db.product_db = db.client[db_name].product
    db.cart_db = db.client[db_name].cart
    logging.info('Base de dados conectada !')

async def disconnect():
    db.client.close()
    logging.info('Base de dados desconectada !')