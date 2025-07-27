from pydantic import BaseModel

from prisma import Prisma


class UpsertDeviceCommand(BaseModel):
    device_id: str
    device_type: str
    device_name: str
    is_connected: bool
    last_seen: int


def create_upsert_device_command_handler(prisma: Prisma):
    async def upsert_device_command_handler(command: UpsertDeviceCommand):
        # Check if device exists
        existing_device = await prisma.device.find_unique(
            where={'id': command.device_id}
        )

        if existing_device:
            # Update existing device
            return await prisma.device.update(
                where={'id': command.device_id},
                data={
                    'is_connected': command.is_connected,
                    'last_seen': command.last_seen,
                    'device_type': command.device_type,
                    'device_name': command.device_name,
                }
            )
        else:
            # Create new device
            return await prisma.device.create(
                data={
                    'id': command.device_id,
                    'device_type': command.device_type,
                    'device_name': command.device_name,
                    'is_connected': command.is_connected,
                    'last_seen': command.last_seen,
                }
            )

    return upsert_device_command_handler
