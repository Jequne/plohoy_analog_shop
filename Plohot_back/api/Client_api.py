from fastapi import APIRouter, Depends, Request, HTTPException, WebSocket, WebSocketDisconnect
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
from services.web_sockets import WebSocketManager

router = APIRouter(prefix="/cart", tags=["cart"])

base_dir = os.path.dirname(os.path.abspath(__file__))
templates_dir = os.path.abspath(os.path.join(base_dir, "../../assets/PP"))

templates = Jinja2Templates(directory=templates_dir)

cart_service = CartService()

ws_manager = WebSocketManager()

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


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await ws_manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)
