import os
import dotenv
import uvicorn

from loguru import logger
from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.config.app_config import create_app
from src.router.user_routes import router as user_router
from src.router.api_routes import router as survey_router
from src.services.scheduler.lazy_scheduler import start_scheduler as start_lazy
from src.services.scheduler.active_scheduler import main as start_active

dotenv.load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start schedulers on startup
    logger.info("n99 server starting...")
    await start_lazy()
    await start_active()
    yield
    logger.info("n99 server shutting down...")

app = create_app(lifespan=lifespan)

app.include_router(user_router)
app.include_router(survey_router)

if __name__ == "__main__":
    uvicorn.run(app, host=os.getenv("HOST"), port=int(os.getenv("PORT")))