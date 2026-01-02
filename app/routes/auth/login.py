from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
import logging
from starlette.status import HTTP_303_SEE_OTHER
from typing import Annotated
from app.services import GetUserService
from app import templates
from app.exceptions import UserNotFoundException, BadCredentialsException


COOKIE_ID = "sid"
COOKIE_EXPIRE = 60 * 60 * 24 * 30
COOKIE_EXPIRE_SHORT = 60 * 30


router = APIRouter()

logger = logging.getLogger("fastapi")


@router.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse(
        request=request, name="login.html", context={"request": request}
    )


@router.post("/do_login", response_class=HTMLResponse)
async def do_login(
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],
    request: Request,
    get_user_service: GetUserService,
    remember_me: Annotated[str | None, Form()] = None,
):
    try:
        user = get_user_service.execute(username, password)
        response = RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)
        max_age = COOKIE_EXPIRE if remember_me == "on" else COOKIE_EXPIRE_SHORT
        response.set_cookie(
            key=COOKIE_ID, value=str(user.id), httponly=True, max_age=max_age
        )
        return response
    except UserNotFoundException as e:
        logger.warning(f"UserNotFoundException: {e} (username: {username})")
        return templates.TemplateResponse(
            request=request,
            name="login.html",
            context={
                "request": request,
                "error": "User not found",
                "username": username,
            },
        )
    except BadCredentialsException as e:
        logger.warning(f"BadCredentialsException: {e} (username: {username})")
        return templates.TemplateResponse(
            request=request,
            name="login.html",
            context={
                "request": request,
                "error": "Invalid credentials",
                "username": username,
            },
        )
