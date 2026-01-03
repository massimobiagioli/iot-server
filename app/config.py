from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    cookie_id: str = "sid"
    cookie_expire: int = 60 * 60 * 24 * 30
    cookie_expire_short: int = 60 * 30

    database_url: str
    database_test_url: str

    class ConfigDict:
        env_file = ".env"