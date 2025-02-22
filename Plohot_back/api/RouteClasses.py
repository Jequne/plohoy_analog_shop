from fastapi import APIRouter, Depends, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from sqlalchemy.future import select
import bcrypt
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.templating import Jinja2Templates
from datetime import datetime, timedelta
import os

from models.products_data import AdminInfo, Product
from helpers.auth_helper import create_access_token, get_current_user
from db.database import get_async_db


# Получение абсолютного пути к директории проекта
base_dir = os.path.dirname(os.path.abspath(__file__))

request_counts = {}

# 🔹 Создаем класс AdminRouter, который расширяет APIRouter
class AdminRouter(APIRouter):
    def __init__(self):
        super().__init__()
        self.add_api_route("/admin/login", self.login_page, methods=["GET"])
        self.add_api_route(
            "/admin/login", self.login, 
            methods=["POST"],
            )
        self.add_api_route("/admin/logout", self.logout, methods=["GET"])


# Получение абсолютного пути к директории проекта
base_dir = os.path.dirname(os.path.abspath(__file__))
templates_dir = os.path.abspath(os.path.join(base_dir, "../../assets/PP"))

# Указание пути к директории шаблонов
templates = Jinja2Templates(directory=templates_dir)

# Класс с базовыми страничками! Которые видны пользователю
class PageRoutes(APIRouter):
    def __init__(self):
        super().__init__()

        self.templates = templates

        self.add_api_route("/plohoy.shop", 
                           self.products_all, 
                           methods=["GET"], 
                           response_class=HTMLResponse
                           )
        self.add_api_route("/About", 
                           self.about, 
                           methods=["GET"], 
                           response_class=HTMLResponse
                           )        
        self.add_api_route("/terms-of-service", 
                           self.terms_serv, 
                           methods=["GET"], 
                           response_class=HTMLResponse
                           )  
        self.add_api_route("/product", 
                           self.product, 
                           methods=["GET"], 
                           response_class=HTMLResponse
                           )

    async def products_all(self, request: Request):
        return self.templates.TemplateResponse("product.html", {"request": request})

    async def about(self, request: Request):
        return self.templates.TemplateResponse("about.html", {"request": request})
        
    async def terms_serv(self, request: Request):
        return self.templates.TemplateResponse("Terms_of_Service.html", {"request": request})

    async def product(self, request: Request):
        return self.templates.TemplateResponse("product.html", {"request": request})

# Класс для логики работы с корзиной и товарами.
class CartLogic(APIRouter):
    def __init__(self):
        super().__init__()
        self.templates = templates

        self.add_api_route("/admin/products", 
                           self.admin_products, 
                           methods=["GET"], 
                           response_class=HTMLResponse
                           )
        self.add_api_route("/admin/products/add", 
                           self.add_product, 
                           methods=["POST"]
                           )
        self.add_api_route("/admin/edit-or-no", 
                           self.edit_or_no, 
                           methods=["GET"]
                           )
        self.add_api_route("/admin/products/delete/{product_id}", 
                           self.delete_product, 
                           methods=["DELETE"]
                           )
        self.add_api_route("/admin/products/edit/{product_id}", 
                           self.edit_product, 
                           methods=["POST"]
                           )

    async def admin_products(self, 
                             request: Request, 
                             db: AsyncSession = Depends(get_async_db), 
                             current_user: str = Depends(get_current_user)
                             ):
        result = await db.execute(select(Product))
        products = result.scalars().all()
        return self.templates.TemplateResponse("admin_products.html", 
                                               {
                                                "request": request, 
                                                "products": products
                                                }
                                               )

    async def add_product(self, 
                          name: str = Form(...), 
                          price: int = Form(...), 
                          quantity: int = Form(...),\
                          db: AsyncSession = Depends(get_async_db), 
                          current_user: str = Depends(get_current_user)
                           ):
        result = await db.execute(select(Product).filter(Product.name == name))
        if result.scalars().first():
            response = RedirectResponse(url="/admin/edit-or-no", 
                                        status_code=303
                                        )
            return response
        add_product = Product(name=name, price=price, quantity=quantity)
        db.add(add_product)
        await db.commit()
        await db.refresh(add_product)
        return HTMLResponse(
                    """
            <!DOCTYPE html>
            <html lang="ru">
            <head>
                <meta charset="UTF-8">
                <title>Успех</title>
            </head>
            <body>
                <h2 style="color: green;">✅ Товар успешно добавлен в базу данных!</h2>
                <a href="/admin/products">Вернуться к списку товаров</a>
            </body>
            </html>
            """
        )

    async def edit_or_no(self, request:Request):
            return HTMLResponse(
                """
                <!DOCTYPE html>
                <html lang="ru">
                <head>
                    <meta charset="UTF-8">
                    <title>Редактирование товара</title>
                </head>
                <body>
                    <h2>Данный товар уже есть в базе данных</h2>
                    <п>Вы хотите что-либо изменить в нем или же нет?</п>
                    
                    <form action="/edit-product" method="get">
                        <button type="submit">Yes</button>
                    </form>
                    
                    <form action="/admin/products" method="get">
                        <button type="submit">No</button>
                    </form>
                </body>
                </html>
                """
                )
    
    async def delete_product(self, 
                             product_id: int, 
                             request: Request, 
                             db: AsyncSession = Depends(get_async_db), 
                             current_user: str = Depends(get_current_user)
                             ):
        # Ищем товар по ID
        result = await db.execute(select(Product).filter(Product.id == product_id))
        product = result.scalars().first()
        # Если товар не найден, возвращаем ошибку
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        # Удаляем товар из базы данных
        await db.delete(product)
        await db.commit()
        # return RedirectResponse(url="/admin/products", status_code=303)
        return JSONResponse(content={"message": "Product deleted successfully"})

    

    async def edit_product(self, 
                           product_id: int, 
                           name: str = Form(...), 
                           price: int = Form(...), 
                           quantity: int = Form(...), 
                           db: AsyncSession = Depends(get_async_db)
                           ):
        # Ищем товар в базе данных
        result = await db.execute(select(Product).filter(Product.id == product_id))
        product = result.scalars().first()
        # Если товар не найден, возвращаем ошибку
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        # Обновляем данные товара
        product.name = name
        product.price = price
        product.quantity = quantity
    # Сохраняем изменения в базе данных
        await db.commit()
        await db.refresh(product)
        return RedirectResponse(url="/admin/products", status_code=303)

    

# Создаем объекты маршрутизатора
admin_router = AdminRouter()
static_routes = PageRoutes()
cart_logic = CartLogic()