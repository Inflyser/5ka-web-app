import ssl
import aiohttp
import asyncio
import logging
import os

from pyaterochka_api import Pyaterochka
from pyaterochka_api import PurchaseMode
from typing import Optional

from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from pydantic import BaseModel
from dotenv import load_dotenv


from router import categories

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

# === SSL PATCH ДЛЯ PYATEROCHKA ===
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

@asynccontextmanager
async def lifespan(app: FastAPI):
    await bot.set_webhook(WEBHOOK_URL)
    yield

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

# === API ДЛЯ ДОСТАВКИ ЧЕРЕЗ PYATEROCHKA_API ===
class Location(BaseModel):
    lat: float
    lon: float

# Схема для второго запроса
class ProductQuery(BaseModel):
    store_id: str
    category_id: str

api_router = APIRouter()

@api_router.post("/get-store-and-categories")
async def check_delivery(loc: Location):
    logger.info(f"Проверка доставки для координат: lat={loc.lat}, lon={loc.lon}")
    try:
        async with Pyaterochka(
            proxy=get_toolip_proxy(),
            debug=True,
            autoclose_browser=False,
            trust_env=False
        ) as API:
            store = await API.find_store(longitude=loc.lon, latitude=loc.lat)
            if store:
                logger.info("Магазин найден")

                catalog = await API.categories_list(
                    subcategories=True,
                    mode=PurchaseMode.DELIVERY
                )
                print(f"Categories list output: {catalog!s:.100s}...\n")
                
                flattened = categories.flatten_categories(catalog)
                categories.flat_categories.clear()
                categories.flat_categories.extend(flattened)
                print(catalog)
                return {
                    "status": "ok",
                    "store": store,
                    "categories": catalog  # Можно также вернуть список категорий
                }
                
            else:
                logger.warning("Нет доступных магазинов")
                raise HTTPException(status_code=404, detail="Магазин не найден по координатам")

    except Exception as e:
        logger.exception("Ошибка при получении магазина через Pyaterochka API")
        raise HTTPException(status_code=500, detail=str(e))
    



@api_router.post("/get-products")
async def get_products(data: ProductQuery):
    logger.info(f"Получение товаров по store_id={data.store_id}, category_id={data.category_id}")
    try:
        async with Pyaterochka(
            proxy=get_toolip_proxy(),
            debug=True,
            autoclose_browser=False,
            trust_env=False
        ) as API:
            # Возможно, потребуется явно выбрать магазин (если библиотека это поддерживает)
            # Если нет — просто вызываем products_list
            products = await API.products_list(
                category_id=data.category_id,
                limit=100
            )

            return {
                "status": "ok",
                "products": products
            }

    except Exception as e:
        logger.exception("Ошибка при получении товаров")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/telegram")
async def telegram_webhook(update: dict):
    telegram_update = Update.model_validate(update)
    await dp.feed_update(bot, telegram_update)
    return {"ok": True}

# === Роутеры ===
app.include_router(api_router)

app.include_router(categories.router)