import time

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from src import mqtt
from src.commands import SendInboundMessageCommand, create_send_inbound_message_command_handler

router = APIRouter(
    prefix="/devices",
    tags=["device-actions"]
)


class PingRequest(BaseModel):
    device_id: str


@router.post("/{device_id}/ping")
async def ping_device(device_id: str):
    """Send a ping command to a specific device"""
    try:
        # Create command handler
        send_message_handler = create_send_inbound_message_command_handler(mqtt.client)
        
        # Create ping command
        ping_command = SendInboundMessageCommand(
            device_id=device_id,
            event_type="ping",
            timestamp=int(time.time())
        )
        
        # Execute command
        result = await send_message_handler(ping_command)
        
        return {
            "success": True,
            "message": f"Ping sent to device {device_id}",
            "topic": result["topic"],
            "payload": result["message"]
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to send ping to device {device_id}: {str(e)}"
        )
