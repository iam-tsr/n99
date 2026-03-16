from fastapi import FastAPI

from .api_routes import router as survey_router

from loguru import logger

app = FastAPI()

app.include_router(survey_router)

@app.get("/health")
async def health_check():
    logger.info("Health check endpoint was called.")
    return {"status": "healthy"}