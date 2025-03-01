from fastapi import FastAPI
import asyncio
from contextlib import asynccontextmanager
from services.web_sockets import WebSocketManager

from services.cart_service import CartService
from db.database import get_async_db

# Создаём экземпляр менеджера WebSocket
ws_manager = WebSocketManager()
cart_service = CartService()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Когда приложение запускается, начинаем фоновую задачу
    task = asyncio.create_task(periodic_updates())  # Периодические обновления
    cart_cleanup_task = asyncio.create_task(periodic_cart_cleanup())  # Очистка корзины
    yield  # Приложение работает
    # Когда приложение завершится, отменяем задачу
    task.cancel()
    cart_cleanup_task.cancel()
    await asyncio.gather(task, cart_cleanup_task, return_exceptions=True)



async def periodic_updates():
    while True:
        await ws_manager.send_product_updates()  # Отправляем обновления всем клиентам
        await asyncio.sleep(10)  # Раз в 10 секунд


async def periodic_cart_cleanup():
    while True:
        async with get_async_db() as db:
            await cart_service.clear_expired_reservations(db)
        await asyncio.sleep(600)  # Каждые 10 минут