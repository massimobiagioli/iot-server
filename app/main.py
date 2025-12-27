from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes.api.health import router as health_router
from app.routes.dashboard import router as dashboard_router

server = FastAPI()

server.mount("/static", StaticFiles(directory="static"), name="static")

server.include_router(health_router, prefix="/api/health")
server.include_router(dashboard_router)
