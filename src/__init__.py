import json
from functools import lru_cache

from fastapi.templating import Jinja2Templates
from fastapi_mqtt import FastMQTT, MQTTConfig

from prisma import Prisma
from src.config import Settings
from src.queries.process_device_status_query import (
    ProcessDeviceStatusQuery,
    create_process_device_status_query_handler,
)


@lru_cache
def get_settings():
    return Settings()


def init_mqtt():
    settings = get_settings()
    return FastMQTT(
        config=MQTTConfig(
            host=settings.mqtt_host,
            port=settings.mqtt_port,
            username=settings.mqtt_user,
            password=settings.mqtt_password,
        )
    )


mqtt = init_mqtt()


@mqtt.on_connect()
def handle_mqtt_connect(client, flags, rc, properties):
    mqtt.client.subscribe("inbound/#")
    mqtt.client.subscribe("device_status")
    print("MQTT connected and subscribed to topics")


@mqtt.subscribe("inbound/#")
async def handle_mqtt_message(client, topic, payload, qos, properties):
    print(
        "Received message to specific topic: ", topic, payload.decode(), qos, properties
    )
    client.publish("outbound/d01", "Hello from Fastapi")


@mqtt.subscribe("device_status")
async def handle_device_status_message(client, topic, payload, qos, properties):
    """Handle device status messages from the device_status queue"""
    try:
        payload_str = payload.decode()
        message = json.loads(payload_str)
        query_handler = create_process_device_status_query_handler(prisma)
        query = ProcessDeviceStatusQuery(message=message)
        await query_handler(query)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON in device status message: {e}")
        print(f"Raw payload: {payload_str}")
    except Exception as e:
        print(f"Error handling device status message: {e}")


templates = Jinja2Templates(directory="templates")

prisma = Prisma()
