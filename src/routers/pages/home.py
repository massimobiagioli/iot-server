from fastapi import APIRouter, Request

from src import prisma, templates
from src.queries.device_stats_query import create_device_stats_query_handler

router = APIRouter()


@router.get("/")
async def index(request: Request):
    device_stats_handler = create_device_stats_query_handler(prisma)
    device_stats = await device_stats_handler()
    
    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context={"device_stats": device_stats}
    )
