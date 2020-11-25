"""Main application."""
from fastapi import FastAPI

from app.api.api import api_router
from app.core.config import settings
from app.home.endpoints import home_router

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(home_router, tags=["home"])
