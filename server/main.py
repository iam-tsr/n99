from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
from contextlib import asynccontextmanager
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from router.api_routes import router as api_router
from config.pg_config import engine
from model.db import models
from router import auth_routes, alert_routes
from services.agent_scheduler import start_scheduler
import logging

logging.basicConfig(level=logging.INFO)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Start APScheduler
    start_scheduler()
    yield
    # Shutdown logic if any

app = FastAPI(title="m99 Cinema Scraper API", lifespan=lifespan)

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": str(exc.detail)},
    )

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logging.error(f"Global Exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": f"Internal Server Error: {str(exc)}"},
    )

# Add CORS so the frontend can retrieve data from localhost
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables
if engine:
    models.Base.metadata.create_all(bind=engine)

# Include the routers directly under /api prefix instead of mounting a sub-app
app.include_router(api_router, prefix="/api")
app.include_router(auth_routes.router, prefix="/api")
app.include_router(alert_routes.router, prefix="/api")

@app.get("/api/health")
async def health_check():
    logging.info("Health check endpoint was called.")
    return {"status": "healthy"}

# Serve the client directory as static files for the frontend
import os
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
client_dir = os.path.join(parent_dir, "client")
if os.path.exists(client_dir):
    app.mount("/", StaticFiles(directory=client_dir, html=True), name="static")
else:
    @app.get("/")
    def read_root():
        return {"message": "Welcome to m99 Cinema Scraper API! Visit /docs for the API documentation."}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
