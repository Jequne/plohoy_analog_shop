from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from slowapi.errors import RateLimitExceeded
from Plohot_back.api.RouteClasses import admin_router, static_routes, cart_logic

app = FastAPI()


app.mount("/assets/css", StaticFiles(directory="../assets/css"), name="css")
app.mount("/assets/img", StaticFiles(directory="../assets/img"), name="img")
app.mount("/assets/scripts-js", StaticFiles(directory="../assets/scripts-js"), name="scripts")

app.include_router(admin_router)
app.include_router(static_routes)
app.include_router(cart_logic)

@app.exception_handler(RateLimitExceeded)
async def rate_limit_error(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Too many requests, please try again later."}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)




