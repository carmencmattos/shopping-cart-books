from fastapi import FastAPI
from api.server.database import connect, disconnect
from api.routers import routers

app = FastAPI()

app.add_event_handler('startup', connect)
app.add_event_handler('shutdown', disconnect)
app.include_router(routers)
