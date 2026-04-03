import os
import dotenv

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from starsessions import SessionMiddleware
from starsessions.stores.redis import RedisStore
from upstash_redis.asyncio import Redis

dotenv.load_dotenv()

redis_client = Redis(url=os.getenv("UPSTASH_REDIS_REST_URL"), token=os.getenv("UPSTASH_REDIS_REST_TOKEN"))

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
            "https://iam-tsr.github.io", # Production
            "http://localhost:5173", # Local test with Vite dev server
            "http://localhost:4173", # Local test with Vite preview
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