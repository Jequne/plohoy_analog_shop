from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from shemas.shemas import ProductAdd, ProductCartDelete
from services.cart import CartLogic

class CartService:
    def __init__(self):
        self.cart_logic = CartLogic()

    async def add_to_cart(self, db: AsyncSession, product_add: ProductAdd):
        try:
            reservation = await self.cart_logic.add_to_cart(db, product_add)
            return {"message": "Product added to cart", "reservation": reservation}
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    async def delete_from_cart(self, 
                               db: AsyncSession,
                               product_cart_delete: ProductCartDelete):
        try:
            await self.cart_logic.delete_from_cart(db, product_cart_delete)
            return {"message": "Product removed from cart"}
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    async def get_cart(self, db: AsyncSession, session_id: str):
        try:
            cart = await self.cart_logic.get_cart(db, session_id)
            return {"cart": cart}
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        
    async def clear_expired_reservations(self, db:AsyncSession):
        await self.cart_logic.clear_expired_reservations(db)
        return {"message": "Expired reservations cleared"}