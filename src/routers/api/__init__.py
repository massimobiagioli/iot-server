from fastapi import APIRouter

from src.routers.api import device_actions, health

router = APIRouter(
    prefix="/api",
    tags=["API"],
)

router.include_router(health.router)
router.include_router(device_actions.router)
