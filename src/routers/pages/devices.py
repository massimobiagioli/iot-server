from fastapi import APIRouter, Request

from src import templates

router = APIRouter(
    prefix="/devices",
)


@router.get("/")
async def index(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="devices.html",
    )
