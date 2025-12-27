from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from app import templates

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        request=request, name="dashboard.html", context={"request": request}
    )
