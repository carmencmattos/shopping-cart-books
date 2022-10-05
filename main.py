import uvicorn
from api.app import app
from api.config import config

if __name__ == "__main__":
    uvicorn.run(app, host=config.APP_HOST)