from functools import lru_cache
from typing import Annotated
from fastapi import Depends
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
from .config import Settings


load_dotenv()

templates = Jinja2Templates(directory="templates")


@lru_cache
def get_settings():
    return Settings()


SettingsProvider = Annotated[Settings, Depends(get_settings)]
