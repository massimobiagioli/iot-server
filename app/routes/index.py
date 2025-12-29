from fastapi import APIRouter
from fastapi.responses import HTMLResponse, RedirectResponse


router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def index():
    return RedirectResponse(url="/dashboard")