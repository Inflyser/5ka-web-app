import logging
import os
from fastapi import FastAPI, HTTPException, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from curl_cffi.requests import AsyncSession
from contextlib import asynccontextmanager

# Загрузка переменных окружения
load_dotenv()

# Настройка логгирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Конфигурация
BOT_TOKEN = os.getenv("BOT_TOKEN")
FRONTEND_URL = "https://5ka-front.netlify.app"
WEBHOOK_URL = "https://fiveka-web-app.onrender.com/telegram"

# Модели данных
class Location(BaseModel):
    lat: float
    lon: float

class StoreRequest(BaseModel):
    store_id: str
    category_id: str

# Инициализация приложения
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Инициализация ресурсов
    logger.info("Starting application")
    yield
    # Очистка ресурсов
    logger.info("Shutting down application")

app = FastAPI(lifespan=lifespan)

# CORS настройки
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Роутер API
api_router = APIRouter()

# Клиент для работы с API Пятерочки
class PyaterochkaClient:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "Referer": "https://5ka.ru/",
        "Origin": "https://5ka.ru",
    }

    async def get_stores(self, lat: float, lon: float):
        url = "https://5d.5ka.ru/api/orders/v1/orders/stores/"
        params = {"lat": lat, "lon": lon}
        
        async with AsyncSession(impersonate="chrome120", verify=False) as session:
            try:
                response = await session.get(
                    url,
                    params=params,
                    headers=self.headers,
                    timeout=10
                )
                response.raise_for_status()
                return response.json()
            except Exception as e:
                logger.error(f"Store fetch error: {e}")
                return None

    async def get_categories(self):
        url = "https://5ka.ru/api/v2/categories/"
        
        async with AsyncSession(impersonate="chrome120", verify=False) as session:
            try:
                response = await session.get(
                    url,
                    headers=self.headers,
                    timeout=10
                )
                response.raise_for_status()
                return response.json()
            except Exception as e:
                logger.error(f"Categories fetch error: {e}")
                return None

    async def get_products(self, store_id: str, category_id: str):
        url = f"https://5ka.ru/api/v2/products/?store={store_id}&category={category_id}"
        
        async with AsyncSession(impersonate="chrome120", verify=False) as session:
            try:
                response = await session.get(
                    url,
                    headers=self.headers,
                    timeout=10
                )
                response.raise_for_status()
                return response.json()
            except Exception as e:
                logger.error(f"Products fetch error: {e}")
                return None

# Эндпоинты API
@api_router.get("/ping")
async def ping():
    return {"status": "ok", "message": "Service is running"}

@api_router.post("/api/stores")
async def get_stores(location: Location):
    client = PyaterochkaClient()
    data = await client.get_stores(location.lat, location.lon)
    if not data:
        raise HTTPException(status_code=500, detail="Failed to fetch stores")
    return {"status": "ok", "data": data}

@api_router.get("/api/categories")
async def get_categories():
    client = PyaterochkaClient()
    data = await client.get_categories()
    if not data:
        raise HTTPException(status_code=500, detail="Failed to fetch categories")
    return {"status": "ok", "data": data}

@api_router.post("/api/products")
async def get_products(request: StoreRequest):
    client = PyaterochkaClient()
    data = await client.get_products(request.store_id, request.category_id)
    if not data:
        raise HTTPException(status_code=500, detail="Failed to fetch products")
    return {"status": "ok", "data": data}

# Подключение роутера
app.include_router(api_router)
