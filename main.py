import ssl
import aiohttp
import asyncio
import logging
import os

from pyaterochka_api import Pyaterochka
from pyaterochka_api import PurchaseMode

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

# === НАСТРОЙКИ ===
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
FRONTEND_URL = "https://5ka-front.netlify.app"
WEBHOOK_URL = "https://fiveka-web-app.onrender.com/telegram"
PROXY_URL = os.getenv("TOOLIP_PROXY")  

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

api_router = APIRouter()

@api_router.post("/check-delivery")
async def check_delivery(loc: Location):
    logger.info(f"Проверка доставки для координат: lat={loc.lat}, lon={loc.lon}")
    try:
        async with Pyaterochka(
            proxy=PROXY_URL,
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
                print(type(catalog))
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
    

@app.post("/telegram")
async def telegram_webhook(update: dict):
    telegram_update = Update.model_validate(update)
    await dp.feed_update(bot, telegram_update)
    return {"ok": True}

# === Роутеры ===
app.include_router(api_router)

app.include_router(categories.router)