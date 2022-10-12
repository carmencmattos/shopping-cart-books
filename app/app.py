from fastapi import FastAPI
from app.server.database import connect, disconnect
from app.routers import routers

app = FastAPI(title='Carrinho de compras - Livros')

app.add_event_handler('startup', connect)
app.add_event_handler('shutdown', disconnect)
app.include_router(routers)
