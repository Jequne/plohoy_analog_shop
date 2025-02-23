from fastapi import WebSocket, WebSocketDisconnect, Depends
from typing import List
import json
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from db.database import get_async_db
from models.products_data import Product


class WebSocketManager():
    def __init__(self):
        self.clients: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.clients.append(websocket)
    
    async def disconnect(self, websocket: WebSocket):
        self.clients.remove(websocket)

    async def broadcast(self, message: str):
        for client in self.clients:
            await client.send_text(message)

    def get_clients(self):
        return self.clients
    
    async def send_product_updates(self, 
                                   db: AsyncSession=Depends(get_async_db) 
                                   ):
        result_ids = await db.execute(select(Product.id))
        ids = result_ids.scalars().all()
        result_quantities = await db.execute(select(Product.quantity))
        quantities = result_quantities.scalars().all()
        for i, q in zip(ids, quantities):
            data = json.dumps({str(i): q})
            await self.broadcast(data)

