from pydantic import BaseModel

from prisma import Prisma


class FindDeviceQuery(BaseModel):
    device_id: str


def create_find_device_query_handler(prisma: Prisma):
    async def find_device_query_handler(query: FindDeviceQuery):
        return await prisma.device.find_unique(where={"id": query.device_id})

    return find_device_query_handler
