from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase


SQLALCHEMY_DATABASE_URL = "sqlite:///../data/sql_app.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autoflush=False, bind=engine)

class Base(DeclarativeBase): pass





if __name__ == "__main__":
    from products_data import Product
    db = SessionLocal()
    product =  db.query(Product).filter(Product.name == 'test_2').first()
    db.delete(product)
    db.commit()
    db.refresh
