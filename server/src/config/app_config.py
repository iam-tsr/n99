import os
import dotenv

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from starsessions import SessionMiddleware
from starsessions.stores.redis import RedisStore
import redis.asyncio as redis

dotenv.load_dotenv()

redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
redis_client = redis.from_url(redis_url, decode_responses=True)

def create_app() -> FastAPI:
    app = FastAPI()

    # Configure Redis for session management
    app.add_middleware(
        SessionMiddleware,
        store=RedisStore(connection=redis_client),
        # secret_key=os.getenv("SESSION_SECRET_KEY")
    )

    # CORS configuration
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app