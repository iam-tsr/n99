from fastapi import APIRouter
from loguru import logger

router = APIRouter()

@router.get("/health")
async def health_check():
    logger.info("Health check endpoint was called.")
    return {"status": "healthy"}