from fastapi import APIRouter, Request

from src import prisma, templates
from src.queries.find_device_query import (
    FindDeviceQuery,
    create_find_device_query_handler,
)
from src.queries.list_devices_query import create_list_devices_query_handler

router = APIRouter(
    prefix="/devices",
)


@router.get("/")
async def index(request: Request):
    query_handler = create_list_devices_query_handler(prisma)
    devices = await query_handler()

    return templates.TemplateResponse(
        request=request,
        name="devices.html",
        context={"devices": devices},
    )


@router.get("/{device_id}")
async def get_device(request: Request, device_id: str):
    query_handler = create_find_device_query_handler(prisma)
    device = await query_handler(query=FindDeviceQuery(device_id=device_id))

    return templates.TemplateResponse(
        request=request,
        name="device_detail.html",
        context={"device": device},
    )
