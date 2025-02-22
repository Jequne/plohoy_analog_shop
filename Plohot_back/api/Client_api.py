from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.templating import Jinja2Templates
from models.products_data import Product
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import os

from shemas.shemas import ProductAdd
from helpers.cart_session_helper import session_create
from db.database import get_async_db
from services.cart_service import CartService

router = APIRouter(prefix="/cart", tags=["cart"])

base_dir = os.path.dirname(os.path.abspath(__file__))
templates_dir = os.path.abspath(os.path.join(base_dir, "../../assets/PP"))

templates = Jinja2Templates(directory="../../assets/PP")

cart_service = CartService()

@router.post("/add-to-cart")
async def add_to_cart(
    product_add: ProductAdd,
    db: AsyncSession = Depends(get_async_db)
    ):
    session_create(product_add)
    return await cart_service.add_to_cart(db, product_add)

@router.delete("/cart/delete-from-cart/{reservation_id}")
async def delete_from_cart(
    reservation_id: int, 
    db: AsyncSession = Depends(get_async_db)
    ):
    return await cart_service.delete_from_cart(db, reservation_id)

@router.get("/cart/get-cart/{session_id}")
async def get_cart(
    session_id: str, 
    db: AsyncSession = Depends(get_async_db)
    ):
    return await cart_service.get_cart(db, session_id)

@router.get("/product/{product_id}", response_class=HTMLResponse)
async def get_product_page(
    product_id: int, 
    request: Request, 
    db: AsyncSession = Depends(get_async_db)
    ):
    result = await db.execute(select(Product).filter(Product.id == product_id))
    product = result.scalars().first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return templates.TemplateResponse(
        "product.html", 
        {"request": request, "product": product}
        )