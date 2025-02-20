from sqlalchemy import  Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
import bcrypt


from Plohot_back.db.database import Base
 

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False) 

    reservations = relationship("Reservation", back_populates="product")



class Reservation(Base):
    __tablename__ = 'reservations'

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    session_id = Column(Integer, nullable=False)  # В данном случае просто указан
    expires_at = Column(DateTime, nullable=False)
    quantity = Column(Integer, nullable=False)

    product = relationship("Product", back_populates="reservations")
    

class AdminInfo(Base):
    __tablename__ = 'Admin'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)

    def set_password(self, password: str):
        self.password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    def check_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode(), self.password_hash.encode())
    













