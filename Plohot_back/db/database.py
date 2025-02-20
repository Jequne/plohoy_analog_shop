from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from settings.settings import get_settings

config = get_settings()
SQLALCHEMY_DATABASE_URL = config.SQLALCHEMY_DATABASE_URL

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False},
    echo=True
)

async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

class Base(DeclarativeBase): pass

async def get_async_db():
    async with async_session() as session:
        yield session


# if __name__ == "__main__":
#     from Plohot_back.models.products_data import Product
#     db = SessionLocal()
#     product =  db.query(Product).filter(Product.name == 'test_2').first()
#     db.delete(product)
#     db.commit()
#     db.refresh
