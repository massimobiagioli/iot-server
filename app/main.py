from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes.api.health import health_router
from app.routes.dashboard import dashboard_router
from app.routes.auth import login_router
from app.routes.index import router as index_router


server = FastAPI()

server.mount("/static", StaticFiles(directory="static"), name="static")

server.include_router(health_router, prefix="/api/health")
server.include_router(dashboard_router, prefix="/dashboard")
server.include_router(login_router, prefix="/auth")
server.include_router(index_router)