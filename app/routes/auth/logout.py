from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER


COOKIE_ID = "sid"


router = APIRouter()


@router.get("/logout")
async def logout():
    response = RedirectResponse(url="/auth/login", status_code=HTTP_303_SEE_OTHER)
    response.delete_cookie(key=COOKIE_ID)
    return response
