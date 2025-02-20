from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime, timedelta, timezone

from models.products_data import Product, Reservation
from shemas.shemas import ProductBase

class CartLogic():
    async def add_to_cart(
                            self, 
                            db: AsyncSession, 
                            ProductBase: ProductBase,
                          ):
        result = await db.execute(
            select(Product).filter(Product.id == ProductBase.product_id)
            )
        product = result.scalars().first()
        
        if not product:
            raise ValueError("Product not found")
        if product.quantity < ProductBase.quantity:
            raise ValueError("Not enough product in stock")
        
        expires_at = datetime.now(timezone.utc) + timedelta(hours=1.5)
        reservation = Reservation(
            product_id=ProductBase.product_id,
            session_id=ProductBase.session_id,
            quantity=ProductBase.quantity,
            expires_at=expires_at
        )
        
        product.quantity -= ProductBase.quantity
        
        db.add(reservation)
        await db.commit()
        await db.refresh(reservation)
        
        return reservation

    async def delete_from_cart(self, db: AsyncSession, reservation_id: int):
        result = await db.execute(
            select(Reservation).filter(Reservation.id == reservation_id)
            )
        reservation = result.scalars().first()
        
        if not reservation:
            raise ValueError("Reservation not found")
        
        result = await db.execute(
            select(Product).filter(Product.id == reservation.product_id)
            )
        product = result.scalars().first()
        
        if product:
            product.quantity += reservation.quantity
        
        await db.delete(reservation)
        await db.commit()

    async def get_cart(self, db: AsyncSession, session_id: str):
        result = await db.execute(
            select(Reservation).filter(Reservation.session_id == session_id)
            )
        reservations = result.scalars().all()
        return reservations