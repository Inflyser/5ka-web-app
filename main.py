import ssl
import aiohttp
import asyncio
import logging
import os
import json
from typing import Optional, List, Dict

from curl_cffi.requests import AsyncSession
from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from pydantic import BaseModel
from dotenv import load_dotenv

from router import categories
from router import products

from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, WebAppInfo, Update
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.exceptions import TelegramForbiddenError

import random
import string

# === НАСТРОЙКИ ===
load_dotenv()

def generate_random_session_id(length: int = 8) -> str:
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def get_toolip_proxy() -> str:
    password = os.getenv("TOOLIP_PROXY")  
    session = generate_random_session_id()
    proxy = f"http://tl-85a86a8ebc70066fa6c97c81acd72f2b9a06dedcca4addf6e9b2395ce556bd41-country-ru-session-{session}:{password}@proxy.toolip.io:31111"
    print(proxy)
    return proxy

BOT_TOKEN = os.getenv("BOT_TOKEN")
FRONTEND_URL = "https://5ka-front.netlify.app"
WEBHOOK_URL = "https://fiveka-web-app.onrender.com/telegram"
PYATEROCHKA_API_URL = "https://5d.5ka.ru/api/orders/v1"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# === TELEGRAM BOT ===
def webapp_builder() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Click",
        web_app=WebAppInfo(url=f"{FRONTEND_URL}/index.html")
    )
    return builder.as_markup()

tg_router = Router()

@tg_router.message(CommandStart())
async def start(message: Message):
    try:
        await message.answer(
            "Starting - Bot correct!",
            reply_markup=webapp_builder()
        )
    except TelegramForbiddenError:
        logger.warning(f"Пользователь {message.from_user.id} заблокировал бота.")

bot = Bot(
    BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()
dp.include_router(tg_router)

class PyaterochkaAPI:
    def __init__(self, proxy: Optional[str] = None):
        self.base_url = PYATEROCHKA_API_URL
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "Referer": "https://5ka.ru/",
            "Origin": "https://5ka.ru",
        }
        self.proxy = proxy
        self.session = None

    async def __aenter__(self):
        self.session = AsyncSession(
            impersonate="chrome120",
            proxy=self.proxy,
            headers=self.headers
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def find_store(self, latitude: float, longitude: float) -> Optional[Dict]:
        url = f"{self.base_url}/orders/stores/"
        params = {
            "lat": latitude,
            "lon": longitude
        }
        
        try:
            response = await self.session.get(url, params=params)
            response.raise_for_status()
            stores = response.json()
            
            if stores and len(stores) > 0:
                return stores[0]  # возвращаем первый магазин
            return None
            
        except Exception as e:
            logger.error(f"Error finding store: {str(e)}")
            return None

    async def get_categories(self) -> Optional[List[Dict]]:
        url = f"{self.base_url}/categories/"
        params = {
            "subcategories": "true",
            "mode": "delivery"
        }
        
        try:
            response = await self.session.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error getting categories: {str(e)}")
            return None

    async def get_products(self, store_id: str, category_id: str, limit: int = 100) -> Optional[Dict]:
        url = f"{self.base_url}/products/"
        params = {
            "category_id": category_id,
            "limit": limit,
            "mode": "delivery",
            "sap_code_store_id": store_id
        }
        
        try:
            response = await self.session.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error getting products: {str(e)}")
            return None

pyaterochka_api = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global pyaterochka_api
    pyaterochka_api = PyaterochkaAPI(proxy=get_toolip_proxy())
    await pyaterochka_api.__aenter__()
    
    yield
    
    await pyaterochka_api.__aexit__(None, None, None)

# === FASTAPI ===
app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/ping")
async def ping():
    return JSONResponse(content={"status": "ok", "message": "Backend is alive!"})

# === API ДЛЯ ДОСТАВКИ ЧЕРЕЗ PYATEROCHKA ===
class Location(BaseModel):
    lat: float
    lon: float

class ProductQuery(BaseModel):
    store_id: str
    category_id: str

api_router = APIRouter()

@api_router.post("/get-store-and-categories")
async def check_delivery(loc: Location):
    try:
        store = await pyaterochka_api.find_store(loc.lat, loc.lon)
        if not store:
            raise HTTPException(status_code=404, detail="Магазин не найден")
            
        catalog = await pyaterochka_api.get_categories()
        if not catalog:
            raise HTTPException(status_code=404, detail="Категории не найдены")
            
        flattened = categories.flatten_categories(catalog)
        categories.flat_categories.clear()
        categories.flat_categories.extend(flattened)
        
        return {
            "status": "ok",
            "store": store,
            "categories": catalog
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/get-products")
async def get_products(data: ProductQuery, limit: int = 100):
    try:
        raw_products = await pyaterochka_api.get_products(
            store_id=data.store_id,
            category_id=data.category_id,
            limit=limit
        )
        
        if not raw_products:
            raise HTTPException(status_code=404, detail="Товары не найдены")
        
        processed_data = products.process_products(raw_products)
        
        # Обновляем хранилище
        products.products_store.clear()
        products.products_store.extend(processed_data["products"])
        
        return JSONResponse({
            "status": "success",
            "count": len(processed_data["products"]),
            "data": processed_data
        })
        
    except Exception as e:
        logger.error(f"Error getting products: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to get products"
        )

@app.post("/telegram")
async def telegram_webhook(update: dict):
    telegram_update = Update.model_validate(update)
    await dp.feed_update(bot, telegram_update)
    return {"ok": True}

# === Роутеры ===
app.include_router(api_router)
app.include_router(categories.router)
app.include_router(products.router)