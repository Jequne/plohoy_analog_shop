from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from slowapi.errors import RateLimitExceeded
import os

from api.RouteClasses import admin_router, static_routes, cart_logic
from api.Client_api import router
from api.on_event import lifespan
from api.products_api import product_route



app = FastAPI(lifespan=lifespan)

# Получение абсолютного пути к корневой директории проекта
base_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(base_dir, ".."))

# Настройка маршрутизации для статических файлов
app.mount("/assets/css", StaticFiles(directory=os.path.join(project_root, "assets/css")), name="css")
app.mount("/assets/img", StaticFiles(directory=os.path.join(project_root, "assets/img")), name="img")
app.mount("/assets/scripts-js", StaticFiles(directory=os.path.join(project_root, "assets/scripts-js")), name="scripts")

app.include_router(admin_router)
app.include_router(static_routes)
app.include_router(cart_logic)
app.include_router(router)
app.include_router(product_route)

@app.exception_handler(RateLimitExceeded)
async def rate_limit_error(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Too many requests, please try again later."}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)


