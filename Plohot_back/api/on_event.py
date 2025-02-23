import asyncio
from contextlib import asynccontextmanager
from services.web_sockets import WebSocketManager

# Создаём экземпляр менеджера WebSocket
ws_manager = WebSocketManager()

@asynccontextmanager
async def lifespan(app):
    # Когда приложение запускается, начинаем фоновую задачу
    task = asyncio.create_task(periodic_updates())  # Периодические обновления
    yield  # Приложение работает
    # Когда приложение завершится, отменяем задачу
    task.cancel()
    await task

async def periodic_updates():
    while True:
        await ws_manager.send_product_updates()  # Отправляем обновления всем клиентам
        await asyncio.sleep(10)  # Раз в 10 секунд