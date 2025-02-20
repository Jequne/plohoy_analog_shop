from fastapi import APIRouter


router = APIRouter()

@router.post("/add_to_cart", prefix='/cart')
async def add_to_cart():
    pass

