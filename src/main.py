from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.routers.api import router as api_router
from src.routers.pages import router as pages_router

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(api_router)
app.include_router(pages_router)
