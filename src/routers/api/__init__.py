from fastapi import APIRouter

from src.routers.api import health

router = APIRouter(
    prefix="/api",
    tags=["API"],
)

router.include_router(health.router)
