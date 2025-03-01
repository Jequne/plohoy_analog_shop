from fastapi.responses import JSONResponse
from fastapi import Request, Response

from shemas.shemas import ProductAdd
import uuid

# def session_create(product_add: ProductAdd):
#     # if product_add.session_id is None:
#     #     session_id = str(uuid.uuid4())  # Генерация уникального session_id
#     #     # Устанавливаем куку с session_id
#     #     response = JSONResponse(content={"message": "Session created"})
#     #     response.set_cookie(key="session_id", value=session_id)
#     #     return JSONResponse(content={"message": "Session created", "session_id": session_id})
#     # return {"message": "Session already exists"}

def session_create_1(request: Request,
                     response: Response,
                     product_add: ProductAdd):
    if request.cookies.get("session_id"):
        return {"message": "Session already exists"}
    
    session_id = str(uuid.uuid4())  # Генерация уникального session_id
    # Устанавливаем куку с session_id
    response.set_cookie(key="session_id", value=session_id)
    product_add.session_id = session_id
    return response