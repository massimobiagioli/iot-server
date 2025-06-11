from functools import lru_cache

from fastapi.templating import Jinja2Templates
from fastapi_mqtt import FastMQTT, MQTTConfig

from prisma import Prisma
from src.config import Settings


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


@mqtt.subscribe("inbound/#")
async def handle_mqtt_message(client, topic, payload, qos, properties):
    print(
        "Received message to specific topic: ", topic, payload.decode(), qos, properties
    )
    client.publish("outbound/d01", "Hello from Fastapi")


templates = Jinja2Templates(directory="templates")

prisma = Prisma()
