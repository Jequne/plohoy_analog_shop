from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.templating import Jinja2Templates
from models.products_data import Product
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.templating import Jinja2Templates

from db.database import get_async_db


product_route = APIRouter()

templates = Jinja2Templates(directory="./../assets/PP")

# ЗАПРОС НА ПОЛУЧЕНИЕ СТРАНИЦЫ С ТОВАРОМ ДЛЯ ДОБАВЛЕНИЯ В КОРЗИНУ И Т.П
@product_route.get("/product/{product_id}")
async def get_product(
    product_id: int,
    request: Request,
    db: AsyncSession = Depends(get_async_db)
    
):

    product = await db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    

    return templates.TemplateResponse(
        f"product-{product_id}.html",
        {
            "request": request,
            "product": product
        }
    )