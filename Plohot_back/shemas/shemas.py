from pydantic import BaseModel
from datetime import datetime
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

from settings.settings import get_settings



class ProductBase(BaseModel):
    name: str
    price: int
    quantity: int






# load_dotenv()
# class AuthSettings(BaseSettings):
#     SECRET_KEY: str
#     ALGORITHM: str

# auth_settings = AuthSettings()


