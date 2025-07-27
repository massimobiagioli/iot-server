import json
from typing import Optional

from pydantic import BaseModel


class SendInboundMessageCommand(BaseModel):
    device_id: str
    event_type: str
    timestamp: int
    payload: Optional[dict] = None


def create_send_inbound_message_command_handler(mqtt_client):
    async def send_inbound_message_command_handler(command: SendInboundMessageCommand):
        """Send a message to the outbound MQTT topic for a specific device"""
        
        # Create message in the same format as inbound messages
        message = {
            "event_type": command.event_type,
            "timestamp": command.timestamp
        }
        
        # Only include payload if it's not None and not empty
        if command.payload:
            message["payload"] = command.payload
        
        # Publish to outbound topic for the specific device
        topic = f"outbound/{command.device_id}"
        message_json = json.dumps(message)
        
        # Send MQTT message
        mqtt_client.publish(topic, message_json.encode("utf-8"), qos=1)
        
        return {
            "success": True,
            "topic": topic,
            "message": message
        }

    return send_inbound_message_command_handler
