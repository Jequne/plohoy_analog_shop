from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from services.cart import CartLogic
from shemas.shemas import ProductAdd
from helpers.cart_session_helper import session_create
from db.database import get_async_db

router = APIRouter(prefix="/cart", tags=["cart"])

@router.post("/add-to-cart")
async def add_to_cart(product_add: ProductAdd,
                      db: AsyncSession = Depends(get_async_db)):
    session_create(product_add)
    try:
        cart_logic = CartLogic()
        reservation = await cart_logic.add_to_cart(db, product_add)
        return {"message": "Product added to cart", "reservation": reservation}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@router.delete("/cart/delete-from-cart/{reservation_id}")
async def delete_from_cart(reservation_id: int, 
                           db: AsyncSession = Depends(get_async_db)
                           ):
    try:
        cart_logic = CartLogic()
        await cart_logic.delete_from_cart(db, reservation_id)
        return {"message": "Product removed from cart"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@router.get("/cart/get-cart/{session_id}")
async def get_cart(session_id: str, 
                   db: AsyncSession = Depends(get_async_db)
                   ):
    try:
        cart_logic = CartLogic()
        cart = await cart_logic.get_cart(db, session_id)
        return {"cart": cart}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
