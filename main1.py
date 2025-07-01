import ssl
import aiohttp
import asyncio
import logging
import os
from curl_cffi.requests import AsyncSession
from typing import Optional
from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from pydantic import BaseModel
from dotenv import load_dotenv
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
    return f"http://tl-28586cb1ec8934abdcbf0e23118f0607dd36f3b474f993049effafbd9c11e2d7-country-ru-session-{session}:{password}@proxy.toolip.io:31112"

BOT_TOKEN = os.getenv("BOT_TOKEN")
FRONTEND_URL = "https://5ka-front.netlify.app"
WEBHOOK_URL = "https://fiveka-web-app.onrender.com/telegram"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# === SSL PATCH ===
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

class PatchedSession(aiohttp.ClientSession):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("connector", aiohttp.TCPConnector(ssl=ssl_context))
        super().__init__(*args, **kwargs)

aiohttp.ClientSession = PatchedSession

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

# === API клиент для Пятерочки ===
class PyaterochkaAPIClient:
    def __init__(self):
        self.session = None
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "Referer": "https://5ka.ru/",
            "Origin": "https://5ka.ru",
        }

    async def __aenter__(self):
        self.session = AsyncSession(
            impersonate="chrome120",
            proxies={"http": get_toolip_proxy(), "https": get_toolip_proxy()},
            verify=False
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def find_store(self, latitude: float, longitude: float):
        url = "https://5d.5ka.ru/api/orders/v1/orders/stores/"
        params = {"lat": latitude, "lon": longitude}
        
        try:
            response = await self.session.get(url, params=params, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            if data.get("results"):
                return data["results"][0]  # Возвращаем первый магазин
            return None
        except Exception as e:
            logger.error(f"Ошибка при поиске магазина: {e}")
            return None

    async def get_categories(self):
        url = "https://5ka.ru/api/v2/categories/"
        try:
            response = await self.session.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Ошибка при получении категорий: {e}")
            return None

    async def get_products(self, store_id: str, category_id: str):
        url = f"https://5ka.ru/api/v2/products/?store={store_id}&category={category_id}"
        try:
            response = await self.session.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Ошибка при получении товаров: {e}")
            return None

# === FastAPI приложение ===
pyaterochka_client = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global pyaterochka_client
    pyaterochka_client = PyaterochkaAPIClient()
    await pyaterochka_client.__aenter__()
    yield
    await pyaterochka_client.__aexit__(None, None, None)

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

# === Модели запросов ===
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
        store = await pyaterochka_client.find_store(loc.lat, loc.lon)
        if not store:
            raise HTTPException(status_code=404, detail="Магазин не найден")
            
        categories = await pyaterochka_client.get_categories()
        if not categories:
            raise HTTPException(status_code=500, detail="Не удалось получить категории")
        
        # Здесь можно добавить обработку категорий как в вашем оригинальном коде
        return {
            "status": "ok",
            "store": store,
            "categories": categories
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/get-products")
async def get_products(data: ProductQuery):
    try:
        products = await pyaterochka_client.get_products(data.store_id, data.category_id)
        if not products:
            raise HTTPException(status_code=500, detail="Не удалось получить товары")
        
        # Здесь можно добавить обработку товаров как в вашем оригинальном коде
        return {
            "status": "ok",
            "products": products
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/telegram")
async def telegram_webhook(update: dict):
    telegram_update = Update.model_validate(update)
    await dp.feed_update(bot, telegram_update)
    return {"ok": True}

# === Роутеры ===
app.include_router(api_router)