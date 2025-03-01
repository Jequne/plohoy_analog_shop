from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime, timedelta, timezone

from models.products_data import Product, Reservation
from shemas.shemas import ProductBase, ProductCartDelete

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
        return {
                "message": "Product added to cart",
                "reservation_id": reservation.id  # Теперь клиент будет знать этот ID
                } 
    

    async def delete_from_cart(self, 
                               db: AsyncSession, 
                               product_cart_delete: ProductCartDelete
                               ):
        cart_session_id = product_cart_delete.session_id
        cart_reservation_id = product_cart_delete.reservation_id
        result = await db.execute(
            select(Reservation).filter(
                Reservation.id == cart_reservation_id,
                Reservation.session_id == cart_session_id
            )
        )

        reservation = result.scalars().first()
        if not reservation:
            raise ValueError("Reservation not found")
        
        product_result = await db.execute(
            select(Product).filter(Product.id == reservation.product_id)
        )

        product = product_result.scalars().first()
        if product:
            product.quantity += reservation.quantity

        await db.delete(reservation)
        await db.commit()
        

