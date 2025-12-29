from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from app import templates
from sqlmodel import select
from app.models import User

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    # TODO: Replace with your actual DB session logic
    session = ...  # get your Session object here
    user = None
    user_id = request.cookies.get("user_id")
    if user_id:
        db_user = session.exec(
            select(User).where(User.id == user_id)
        ).first()  # Replace with your DB query logic
        if db_user:
            user = {"username": db_user.username, "role": db_user.role}
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={"request": request, "user": user},
    )
