"""API endpoints."""
from fastapi import APIRouter

from app.api.endpoints import hamqth

api_router = APIRouter()
api_router.include_router(hamqth.router, prefix="/hamqth", tags=["HamQTH"])
