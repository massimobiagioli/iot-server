from typing import Dict

from prisma import Prisma


def create_device_stats_query_handler(prisma: Prisma):
    async def device_stats_query_handler() -> Dict[str, int]:
        """
        Get device statistics: total count and connected count
        """
        total_devices = await prisma.device.count()
        connected_devices = await prisma.device.count(
            where={"is_connected": True}
        )
        
        return {
            "total": total_devices,
            "connected": connected_devices,
            "disconnected": total_devices - connected_devices
        }

    return device_stats_query_handler
