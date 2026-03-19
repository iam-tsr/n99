import uvicorn
from src.config.app_config import create_app
from src.router.user_routes import router as user_router
from src.router.api_routes import router as survey_router

# Create the app ONCE here
app = create_app()

# Include all your routers here
app.include_router(user_router)
app.include_router(survey_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)