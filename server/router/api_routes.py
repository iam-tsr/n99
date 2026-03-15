from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any

from model.core.showing_spider import movies_showing
from model.core.avail_spider import avail_movies

from datetime import datetime

from loguru import logger

router = APIRouter()

# API Schemas
class ShowingRequest(BaseModel):
    name: str  
    code: str 
    city: str 
    date: str 

# API endpoints
@router.post("/search/showing")
async def get_showing_movies(req: ShowingRequest):
    try:
        logger.info(f"Scraping BookMyShow for {req.name} on {req.date}")
        movies = movies_showing(name=req.name, code=req.code, city=req.city, date=req.date)
        return {"movies": movies, "count": len(movies)}
    except Exception as e:
        logger.error(f"Error scraping showing movies: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/search/available")
async def get_available_movies():
    try:
        logger.info("Scraping Inox for available movies")
        movies = avail_movies()
        return {"movies": movies, "count": len(movies)}
    except Exception as e:
        logger.error(f"Error scraping available movies: {e}")
        raise HTTPException(status_code=500, detail=str(e))