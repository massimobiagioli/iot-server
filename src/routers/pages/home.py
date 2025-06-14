from fastapi import APIRouter, Request

from src import templates

router = APIRouter()


@router.get("/")
async def index(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="home.html",
    )
