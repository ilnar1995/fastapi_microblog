import asyncio
from fastapi import FastAPI, Depends
from starlette.requests import Request
from starlette.responses import Response
#from core.db import SessionLocal
from src.core.db import async_session_maker

from src.routes import routes
from src.user.base_config import current_user
from src.user.models import User

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

# приветствие пользователя
@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.username}"

@app.middleware("http")
async def db_session_middleware(request: Request, call_next):   #для создания сессии при каждом запросе в api
    response = Response("Internal server error", status_code=500)
    try:
        # request.state.db = SessionLocal()  # для синхрон запросов
        request.state.db = async_session_maker()  # для асинхрон запросов
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response


app.include_router(routes)

