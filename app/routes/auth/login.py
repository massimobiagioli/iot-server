from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
import logging
from starlette.status import HTTP_303_SEE_OTHER
from typing import Annotated
from app.services import GetUserService
from app import SettingsProvider, templates
from app.exceptions import UserNotFoundException, BadCredentialsException


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
    settings: SettingsProvider,
    remember_me: Annotated[str | None, Form()] = None,
):
    try:
        user = get_user_service(username, password)
        response = RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)
        max_age = (
            settings.cookie_expire
            if remember_me == "on"
            else settings.cookie_expire_short
        )
        response.set_cookie(
            key=settings.cookie_id, value=str(user.id), httponly=True, max_age=max_age
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
