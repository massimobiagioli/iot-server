import os
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

DEFAULT_MQTT_HOST = "127.0.0.1"
DEFAULT_MQTT_PORT = 1883

stage = os.getenv("STAGE", "dev").lower()


def get_env_file() -> str:
    stage_env_file = f".env.{stage}"
    if Path(stage_env_file).exists():
        return stage_env_file

    return ".env"


class Settings(BaseSettings):
    mqtt_host: str = DEFAULT_MQTT_HOST
    mqtt_port: int = DEFAULT_MQTT_PORT
    mqtt_user: str
    mqtt_password: str

    db_url: str

    is_testing_mode: bool = stage == "test"

    model_config = SettingsConfigDict(
        env_file=get_env_file(), env_file_encoding="utf-8"
    )
