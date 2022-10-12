import uvicorn
from app.app import app
from app.config import config

if __name__ == "__main__":
    uvicorn.run(app, host=config.APP_HOST)