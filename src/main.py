from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src import get_settings, mqtt, prisma
from src.routers.api import router as api_router
from src.routers.pages import router as pages_router


@asynccontextmanager
async def _lifespan(_app: FastAPI):
    settings = get_settings()

    if not prisma.is_connected():
        await prisma.connect()

    if not settings.is_testing_mode:
        await mqtt.mqtt_startup()

    yield

    if not settings.is_testing_mode:
        await mqtt.mqtt_shutdown()

    if prisma.is_connected():
        await prisma.disconnect()


app = FastAPI(lifespan=_lifespan)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(api_router)
app.include_router(pages_router)
