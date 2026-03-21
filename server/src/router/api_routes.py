import json

from fastapi import APIRouter
from loguru import logger

from src.services.scheduler.active_scheduler import main
from src.services.scheduler.lazy_scheduler import start_scheduler

from src.model.db.data_pg import DataPG

router = APIRouter()

# API endpoints

@router.get("/api/active-scheduler")
async def get_active_scheduler():
    await main()
    return {"message": "Active scheduler is running."}

@router.get("/api/lazy-scheduler")
async def get_lazy_scheduler():
    start_scheduler()
    return {"message": "Lazy scheduler is running."}

@router.post("/api/listed-movies")
async def get_listed_movies():
    data_pg = DataPG()
    data = data_pg.read_listed_movies()
    return {"movies": data}

@router.post("/api/listed-cinemas")
async def get_listed_cinemas():
    try:
        with open('src/services/scheduler/cinema-list.json', 'r') as f:
            data = json.load(f)
            cinema_names = list(data.get('cinema', {}).keys())
            logger.info("Fetched listed cinema names.")
    except Exception as e:
        logger.error(f"Error fetching listed cinemas: {e}")
        cinema_names = []
    
    return {"cinemas": cinema_names}