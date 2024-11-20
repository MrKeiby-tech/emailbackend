import sentry_sdk
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from api.v1 import templates
import os 
from dotenv import load_dotenv
from core.config import Config


# # Инициализация Sentry
# sentry_sdk.init(
#     dsn=Config.SERNTRYDNS,
#     traces_sample_rate=1.0, 
#     _experiments={
#         "continuous_profiling_auto_start": True,
#     },
# )

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # Разрешённые источники
    allow_credentials=True,
    allow_methods=["*"],  # Разрешённые методы (GET, POST, DELETE и т.д.)
    allow_headers=["*"],  # Разрешённые заголовки
)

# Добавление Sentry Middleware
# app.add_middleware(SentryAsgiMiddleware)

# Подключение маршрутов
app.include_router(templates.router, prefix="/api/templates")

@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}

# Для тестирования ошибок
@app.get("/error")
async def trigger_error():
    return {"message": "Hello, World!"}
