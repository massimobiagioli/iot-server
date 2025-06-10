from functools import lru_cache

from fastapi.templating import Jinja2Templates
from fastapi_mqtt import FastMQTT, MQTTConfig

from src.config import Settings

from prisma import Prisma


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

templates = Jinja2Templates(directory="templates")

prisma = Prisma()
