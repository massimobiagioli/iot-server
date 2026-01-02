from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER
from app import SettingsProvider


router = APIRouter()


@router.get("/logout")
async def logout(
    settings: SettingsProvider,
):
    response = RedirectResponse(url="/auth/login", status_code=HTTP_303_SEE_OTHER)
    response.delete_cookie(key=settings.cookie_id)
    return response
