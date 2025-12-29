from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse

router = APIRouter()


@router.get("/", response_class=None)
async def index(request: Request):
    current_user = getattr(request.state, "current_user", None)
    if current_user:
        return RedirectResponse(url="/dashboard")
    else:
        return RedirectResponse(url="/auth/login")
