import uuid
import json
import redis
from fastapi import APIRouter, Response, HTTPException, Request
from pydantic import BaseModel
from loguru import logger

from src.model.db.profile_pg import ProfilePG
from src.model.db.data_pg import DataPG
from src.config.app_config import redis_client

profile_pg = ProfilePG()
data_pg = DataPG()

router = APIRouter()

class MovieSelection(BaseModel):
    movie: str
    date: str
    cinema: str

class UserProfileRequest(BaseModel):
    temp_key: str
    username: str = None
    email: str = None

@router.get("/health")
async def health_check():
    logger.info("Health check endpoint was called.")
    return {"status": "healthy"}

@router.post("/movie-selection")
async def save_movie_selection(data: MovieSelection):
    logger.info("Movie selection endpoint was called (Page 1).")
    
    # 1. Store movie name, date, cinema & job_id in Redis with a temporary key
    job_id = str(uuid.uuid4())
    temp_key = str(uuid.uuid4())
    movie_info = {
        "movie": data.movie,
        "date": data.date,
        "cinema": data.cinema,
        "job_id": job_id
    }
    
    # Store for 30 minutes
    await redis_client.setex(temp_key, 1800, json.dumps(movie_info))

    # Return the temporary key so the frontend can send it on Page 2
    return temp_key

@router.post("/user-profile")
async def complete_user_registration(data: UserProfileRequest, response: Response, request: Request):
    logger.info("User profile endpoint was called (Page 2).")

    # Check for session_token cookie
    session_token = request.cookies.get("session_token")
    user_id = None
    if session_token:
        user_id = await redis_client.get(f"session:{session_token}")
        logger.info(f"Existing session found for user_id {user_id}. Using existing profile.")
    
    # Fetch movie data from Redis using the temporary key
    movie_info_str = await redis_client.get(data.temp_key)
    if not movie_info_str:
        raise HTTPException(status_code=400, detail="Temporary session expired or invalid.")
    movie_info = json.loads(movie_info_str)

    # If user_id is not found in session, create user profile
    if not user_id:
        if not data.username or not data.email:
            raise HTTPException(status_code=400, detail="Username and email required for new user.")
        user_id = profile_pg.create_user_profile(data.username, data.email)
        session_token = str(uuid.uuid4())
        await redis_client.set(f"session:{session_token}", user_id)
        response.set_cookie(key="session_token", value=session_token, httponly=True)
        logger.info(f"Created new user profile with user_id {user_id} and set session cookie.")

    # Insert user data using the id from previous step and movie data retrieved from Redis
    data_pg.create_user_data(user_id, movie_info["movie"], movie_info["date"], movie_info["cinema"], movie_info["job_id"])

    return {"message": "User account created and data saved."}