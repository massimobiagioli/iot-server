from fastapi import APIRouter

from src.routers.pages import devices, home

router = APIRouter(
    prefix="",
    tags=["Pages"],
)

router.include_router(home.router)
router.include_router(devices.router)
