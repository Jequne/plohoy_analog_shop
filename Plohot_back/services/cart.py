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
        result = await db.execute(
            select(Reservation).filter(
            Reservation.product_id == product_base.product_id,
            Reservation.session_id == product_base.session_id
            )
        )
        existing_reservation = result.scalars().first()
        if existing_reservation:
            # Если резервация существует, обновляем количество
            existing_reservation.quantity += product_base.quantity
            existing_reservation.expires_at = datetime.now(timezone.utc) + timedelta(hours=1.5)
            await db.commit()
            await db.refresh(existing_reservation)
            return existing_reservation
        else:
            # Если резервации нет, создаем новую
            expires_at = datetime.now(timezone.utc) + timedelta(hours=1.5)
            reservation = Reservation(
                product_id=product_base.product_id,
                session_id=product_base.session_id,
                quantity=product_base.quantity,
                expires_at=expires_at
            )
            product.quantity -= product_base.quantity
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
    

    async def clear_expired_reservations(db: AsyncSession):
        result = await db.execute(
            select(Reservation).filter(Reservation.expires_at < datetime.now(timezone.utc))
            )
        reservations = result.scalars().all()
        for reservation in reservations:
            result = await db.execute(
                select(Product).filter(Product.id == reservation.product_id)
                )
            product = result.scalars().first()
            product.quantity += reservation.quantity
            await db.delete(reservation)
        await db.commit()