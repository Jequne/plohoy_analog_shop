from fastapi import APIRouter, Depends, Request, HTTPException, WebSocket, WebSocketDisconnect, BackgroundTasks
from fastapi.templating import Jinja2Templates
from models.products_data import Product
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import os
from starlette.templating import Jinja2Templates

from shemas.shemas import ProductAdd
from helpers.cart_session_helper import session_create
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


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await ws_manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)


@router.get("/clear-expired")
async def clear_expired_reservations(
    background_tasks: BackgroundTasks, 
    db: AsyncSession = Depends(get_async_db)
    ):
    # Добавляем задачу очистки в фоновый режим
    background_tasks.add_task(cart_service.clear_expired_reservations, db)
    return {"message": "Expired reservations are being cleared."}

