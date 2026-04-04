import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from loguru import logger
from src.config.app_config import create_app
from src.router.user_routes import router as user_router
from src.router.api_routes import router as survey_router
from src.services.scheduler.lazy_scheduler import start_scheduler as start_lazy
from src.services.scheduler.active_scheduler import main as start_active

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start schedulers on startup
    logger.info("n99 server starting...")
    await start_lazy()
    await start_active()
    yield
    logger.info("n99 server shutting down...")

# Create the app ONCE here
app = create_app(lifespan=lifespan)

# Include all your routers here
app.include_router(user_router)
app.include_router(survey_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)