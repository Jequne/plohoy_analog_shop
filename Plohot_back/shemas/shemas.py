from fastapi import Cookie, Response
from pydantic import BaseModel
from datetime import datetime
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

from settings.settings import get_settings



class ProductBase(BaseModel):
    name: str
    price: int
    quantity: int
    product_id: int
    session_id: str=Cookie(None)

    class Config:
        arbitrary_types_allowed = True

class ProductAdd(ProductBase):
    pass
    
    class Config:
        arbitrary_types_allowed = True


class ProductCartDelete(BaseModel):
    reservation_id: int
    session_id: str
    
    class Config:
        arbitrary_types_allowed = True
