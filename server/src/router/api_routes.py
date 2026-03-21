import json

from fastapi import APIRouter
from loguru import logger

from src.model.db.data_pg import DataPG
from src.services.scheduler.active_scheduler import main as start_active
from src.config.app_config import redis_client

router = APIRouter()

# API endpoints

@router.get("/api/active-scheduler")
async def get_active_scheduler():
    await start_active()
    return {"message": "Active scheduler triggered."}

@router.get("/api/listed-movies")
async def get_listed_movies():
    cache_key = "listed_movies"
    
    # Try to get from Redis cache
    cached_data = await redis_client.get(cache_key)
    if cached_data:
        return {"movies": json.loads(cached_data)}
    
    # Fetch from database
    data_pg = DataPG()
    data = data_pg.read_listed_movies()
    
    # Store in Redis with 1 hour expiry (3600 seconds)
    await redis_client.setex(cache_key, 3600, json.dumps(data))
    
    return {"movies": data}

@router.get("/api/listed-cinemas")
async def get_listed_cinemas():
    cache_key = "listed_cinemas"
    
    # Try to get from Redis cache
    cached_data = await redis_client.get(cache_key)
    if cached_data:
        return {"cinemas": json.loads(cached_data)}
    
    # Fetch from JSON file
    try:
        with open('src/services/scheduler/cinema-list.json', 'r') as f:
            data = json.load(f)
            cinema_names = list(data.get('cinema', {}).keys())
    except Exception as e:
        logger.error(f"Error fetching listed cinemas: {e}")
        cinema_names = []
    
    # Store in Redis with 1 hour expiry (3600 seconds)
    await redis_client.setex(cache_key, 3600, json.dumps(cinema_names))
    
    return {"cinemas": cinema_names}