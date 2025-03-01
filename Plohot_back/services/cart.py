from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime, timedelta, timezone

from models.products_data import Product, Reservation
from shemas.shemas import ProductBase

class CartLogic():
    
    
    async def add_to_cart(
                            self, 
                            db: AsyncSession, 
                            product_base: ProductBase,
                          ):
        result = await db.execute(
            select(Product).filter(Product.id == product_base.product_id)
            )
        product = result.scalars().first()
        if not product:
            raise ValueError("Product not found")
        if product.quantity < product_base.quantity:
            raise ValueError("Not enough product in stock")

        # Создание новой резервации
        expires_at = datetime.now(timezone.utc) + timedelta(hours=1.5)
        reservation = Reservation(
            product_id=product_base.product_id,
            session_id=product_base.session_id,
            quantity=product_base.quantity,
            expires_at=expires_at
        )

        # Обновляем количество товара в базе
        product.quantity -= product_base.quantity

        # Добавляем в базу данных новую резервацию
        db.add(reservation)
        await db.commit()
        await db.refresh(reservation)

        return reservation


