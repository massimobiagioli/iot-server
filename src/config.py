from pydantic_settings import BaseSettings, SettingsConfigDict


DEFAULT_MQTT_HOST = "127.0.0.1"
DEFAULT_MQTT_PORT = 1883


class Settings(BaseSettings):
    mqtt_host: str = DEFAULT_MQTT_HOST
    mqtt_port: int = DEFAULT_MQTT_PORT
    mqtt_user: str
    mqtt_password: str

    db_url: str

    model_config = SettingsConfigDict(env_file=".env")
