from fastapi import Response
from fastapi.responses import JSONResponse

from shemas.shemas import ProductAdd
import uuid

def session_create(product_add: ProductAdd):
    if product_add.session_id is None:
        session_id = str(uuid.uuid4())  # Генерация уникального session_id
        # Устанавливаем куку с session_id
        response = JSONResponse(content={"message": "Session created"})
        response.set_cookie(key="session_id", value=session_id)
        product_add.session_id = session_id  # Записываем session_id в объект
        return response
    return {"message": "Session already exists"}
