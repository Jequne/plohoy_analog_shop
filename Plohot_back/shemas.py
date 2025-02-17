from pydantic import BaseModel
from datetime import datetime
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os


class ProductBase(BaseModel):
    name: str
    price: int
    quantity: int

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int
    class Config:
        from_attributes = True

class ReservationBase(BaseModel):
    product_id: int
    quantity: int

class ReservationCreate(ReservationBase):
    pass 

class ReservationResponse(ReservationBase):
    id: int
    expires_at: datetime
    class Config:
        from_attributes = True


load_dotenv()
class AuthSettings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str

auth_settings = AuthSettings()


