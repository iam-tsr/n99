from fastapi import APIRouter
from loguru import logger

from src.services.scheduler.active_scheduler import main
from src.services.scheduler.lazy_scheduler import start_scheduler


router = APIRouter()

# API endpoints

@router.get("/active-scheduler")
async def get_active_scheduler():
    await main()
    
    return {"message": "Active scheduler is running."}

@router.get("/lazy-scheduler")
async def get_lazy_scheduler():
    start_scheduler()
    return {"message": "Lazy scheduler is running."}