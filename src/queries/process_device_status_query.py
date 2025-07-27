from typing import Any, Dict

from pydantic import BaseModel

from prisma import Prisma
from src.commands.upsert_device_command import (
    UpsertDeviceCommand,
    create_upsert_device_command_handler,
)


class ProcessDeviceStatusQuery(BaseModel):
    message: Dict[str, Any]


def create_process_device_status_query_handler(prisma: Prisma):
    async def process_device_status_query_handler(query: ProcessDeviceStatusQuery):
        """
        Process device status messages from the device_status queue.
        Expected message format:
        {
            'payload': {
                'device_type': 'esp32',
                'device_id': '0c4f5500',
                'device_name': 'tester'
            },
            'timestamp': 806226802,
            'event_type': 'connected' | 'disconnected'
        }
        """
        try:
            message = query.message
            payload = message.get("payload", {})
            device_id = payload.get("device_id")
            device_type = payload.get("device_type")
            device_name = payload.get("device_name")
            timestamp = message.get("timestamp")
            event_type = message.get("event_type")

            if not all([device_id, device_type, device_name, timestamp, event_type]):
                print(f"Invalid device status message: {message}")
                return None

            is_connected = event_type == "connected"

            # Use the upsert command to create or update the device
            upsert_command_handler = create_upsert_device_command_handler(prisma)
            command = UpsertDeviceCommand(
                device_id=device_id,
                device_type=device_type,
                device_name=device_name,
                is_connected=is_connected,
                last_seen=timestamp,
            )

            device = await upsert_command_handler(command)
            print(f"Processed device {device_id} status to {event_type}")
            return device

        except Exception as e:
            print(f"Error processing device status message: {e}")
            print(f"Message: {message}")
            return None

    return process_device_status_query_handler
