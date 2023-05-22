import asyncio
from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response
from core.db import SessionLocal

from routes import routes

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.middleware("http")
async def db_session_middleware(request: Request, call_next):   #для создания сессии при каждом запросе в api
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response


app.include_router(routes)

