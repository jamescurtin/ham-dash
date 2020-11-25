"""Root endpoints."""
from fastapi import APIRouter

home_router = APIRouter()


@home_router.get("/")
def read_root():
    """Demo hello world entrypoint."""
    return {"Hello": "World"}
