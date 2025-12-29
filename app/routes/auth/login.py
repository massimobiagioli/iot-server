from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from typing import Annotated
from fastapi import Depends
from app.services import GetUser
from app import templates


router = APIRouter()


@router.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse(
        request=request, name="login.html", context={"request": request}
    )


@router.post("/do_login", response_class=HTMLResponse)
async def do_login(
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],
    get_user_service: Annotated[GetUser, Depends()],
    remember_me: Annotated[str | None, Form()] = None,
):
    remember_me_bool = remember_me == "on"
    print("Login attempt:", username, password, remember_me_bool)

    # Test service injection
    user = get_user_service.execute(username, password)
    print("User from service:", user)

    # error = None
    # if not username or not password:
    #     error = "Username and password required."
    # else:
    #     session = Session()  # Assumes Session() is available/configured
    #     user = session.exec(select(User).where(User.username == username)).first()
    #     if not user or not verify_password(password, user.password):
    #         error = "Invalid credentials."

    # if error:
    #     return templates.TemplateResponse(
    #         request=request,
    #         name="login.html",
    #         context={"request": request, "error": error, "username": username}
    #     )

    # expire = 60 * 60 * 24 * (30 if remember_me else 1)
    # response = templates.TemplateResponse(
    #     request=request,
    #     name="login.html",
    #     context={"request": request}
    # )
    # response.set_cookie(key="user_id", value=str(user.id), httponly=True, max_age=expire)
    # response.headers["Location"] = "/"
    # response.status_code = 303
    # return response
