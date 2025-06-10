from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.routers.api import router as api_router
from src.routers.pages import router as pages_router
from src import mqtt, prisma


@asynccontextmanager
async def _lifespan(_app: FastAPI):
    await prisma.connect()
    await mqtt.mqtt_startup()
    yield
    await mqtt.mqtt_shutdown()
    await prisma.disconnect()


app = FastAPI(lifespan=_lifespan)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(api_router)
app.include_router(pages_router)
