from fastapi import APIRouter

from src.routers.pages import home

router = APIRouter(
    prefix="",
    tags=["Pages"],
)

router.include_router(home.router)
