import os
import dotenv

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from starsessions import SessionMiddleware
from starsessions.stores.redis import RedisStore
import redis.asyncio as redis

dotenv.load_dotenv()

redis_client = redis.from_url(os.getenv("REDIS_URL"), decode_responses=True)

def create_app(lifespan=None) -> FastAPI:
    app = FastAPI(lifespan=lifespan)

    # Configure Redis for session management
    app.add_middleware(
        SessionMiddleware,
        store=RedisStore(connection=redis_client),
        # secret_key=os.getenv("SESSION_SECRET_KEY")
    )

    # CORS configuration
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "https://iam-tsr.github.io/n99/",
            "http://localhost:5173",
            "http://127.0.0.1:5173",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app



if __name__ == "__main__":
    async def main():
        app = create_app()
        print("App created successfully.")

        # await redis_client.set("status", "running")
        # print(await redis_client.get("status"))

    import asyncio
    asyncio.run(main())