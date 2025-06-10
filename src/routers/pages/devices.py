from fastapi import APIRouter, Request

from src import templates, prisma

router = APIRouter(
    prefix="/devices",
)


@router.get("/")
async def index(request: Request):
    devices = await prisma.device.find_many()

    return templates.TemplateResponse(
        request=request,
        name="devices.html",
        context={"devices": devices},
    )


@router.get("/{device_id}")
async def get_device(request: Request, device_id: str):
    device = await prisma.device.find_unique(
        where={"id": device_id}
    )

    return templates.TemplateResponse(
        request=request,
        name="device_detail.html",
        context={"device": device},
    )