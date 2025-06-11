from prisma import Prisma


def create_list_devices_query_handler(prisma: Prisma):
    async def list_devices_query_handler():
        return await prisma.device.find_many()

    return list_devices_query_handler
