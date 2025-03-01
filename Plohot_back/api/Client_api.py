from fastapi import APIRouter, Depends, Request, HTTPException, WebSocket, WebSocketDisconnect, BackgroundTasks, Response
from fastapi.templating import Jinja2Templates
from models.products_data import Product
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import os
from starlette.templating import Jinja2Templates

from shemas.shemas import ProductAdd
from helpers.cart_session_helper import  session_create_1
from db.database import get_async_db
from services.cart_service import CartService
from services.web_sockets import WebSocketManager


router = APIRouter()

cart_service = CartService()

ws_manager = WebSocketManager()

templates = Jinja2Templates(directory="../../assets/PP")

@router.post("/add-to-cart/{product_id}")
async def add_to_cart(
    product_add: ProductAdd,
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_async_db),
):
    session_create_1(request=request, 
                     response=response, 
                     product_add=product_add
                     )
    return await cart_service.add_to_cart(db, product_add)
    







@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await ws_manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)



