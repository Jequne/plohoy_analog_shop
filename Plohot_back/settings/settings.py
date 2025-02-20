import os
import sys
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
        if (
        sys.platform.lower() == "win32"
        or os.name.lower() == "nt"
        or os.name.lower() == "posix"
    ):
            from dotenv import load_dotenv
            load_dotenv()
        SECRET_KEY: str = Field(..., env="SECRET_KEY")
        ALGORITHM: str = Field(..., env="ALGORITHM")
        SQLALCHEMY_DATABASE_URL: str = Field(..., env="SQLALCHEMY_DATABASE_URL")


setting: Settings | None = None

def get_settings() -> Settings:
    global setting
    if setting is None:
        setting = Settings()
    return setting