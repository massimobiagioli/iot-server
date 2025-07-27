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

    # Convert Prisma objects to dictionaries for JSON serialization
    devices_dict = []
    for device in devices:
        device_dict = {
            "id": device.id,
            "device_type": device.device_type,
            "device_name": device.device_name,
            "is_connected": device.is_connected,
            "last_seen": device.last_seen,
            "created_at": device.created_at.isoformat() if device.created_at else None,
            "updated_at": device.updated_at.isoformat() if device.updated_at else None,
        }
        devices_dict.append(device_dict)

    return templates.TemplateResponse(
        request=request,
        name="devices.html",
        context={"devices": devices_dict},
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
