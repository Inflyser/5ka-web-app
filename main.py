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

import logging
import os
import httpx

# === НАСТРОЙКИ ===
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
FRONTEND_URL = "https://5ka-front.netlify.app"
WEBHOOK_URL = "https://fiveka-web-app.onrender.com/telegram"

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

# === API ДЛЯ ДОСТАВКИ ===
class Location(BaseModel):
    lat: float
    lon: float

api_router = APIRouter()

@api_router.post("/check-delivery")
async def check_delivery(loc: Location):
    logger.info(f"Получены координаты: lat={loc.lat}, lon={loc.lon}")

    # Формируем URL с координатами, округляя их до 6 знаков
    store_url = (
        f"https://5d.5ka.ru/api/orders/v1/orders/stores/?"
        f"lon={loc.lon}&lat={loc.lat}"
    )
    base_url = "https://5ka.ru"

    HEADERS = {
        "x-app-version": "0.1.1.dev",
        "x-device-id": "afc296b4-0312-461f-98cd-e1755c4ed629",
        "x-platform": "webapp",
        "origin": base_url,
        "user-agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
        ),
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    }

    # Подставь свои актуальные куки из браузера
    COOKIES = {
        "server_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ0b2tlbiIsInNlc3Npb25JZCI6IjY4MGVlNjA0NWRiNWZhOTY4Y2NhYzlhYTliYzM2MTA5NGZkYjM0ZmU0OTAyY2YwMWM4NTdiNzVkYzk4ZWNlNDAiLCJleHAiOjE3NTA1NDc3NDAsImlhdCI6MTc1MDQ2MTM0MCwianRpIjoiZDEzOGQzYjQtMTE4NC00YWE5LWFjNWQtNjJmYTQ4YTAwZjEyIn0.xWqcAGRzsS9fGfBSwZLAqX8cf6DIeT2ftstnFycwXS8",
        "sessionid": "3:1750168435.5.0.1749907214924:PYN0vA:5fef.1.2:1|1076966228.0.2.3:1749907214|3:10309105.877871.yZNVHfFPxx9JFtUIV2bImg78jBE",
        "session_token_timestamp": "1750547740456",
        # Добавь остальные куки, если нужно
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(store_url, headers=HEADERS, cookies=COOKIES)

            logger.info(f"Ответ от 5ka API: {response.status_code} — {response.text}")

            response.raise_for_status()  # выбросит ошибку при 4xx/5xx

            data = response.json()

            if "results" in data and len(data["results"]) > 0:
                logger.info("Магазин(ы) найдены, доставка доступна")
                return {"status": "ok", "store": data["results"][0]}  # или весь список, если нужно
            else:
                logger.warning("Магазины не найдены по координатам")
                raise HTTPException(status_code=404, detail="В вашем районе доставка недоступна")

    except httpx.HTTPStatusError as e:
        logger.error(f"Ошибка HTTP от 5ka: {e.response.status_code} — {e.response.text}")
        raise HTTPException(status_code=500, detail="Ошибка от сервера 5ka")

    except httpx.RequestError as e:
        logger.error(f"Ошибка соединения с 5ka API: {e}")
        raise HTTPException(status_code=500, detail="Проблема с подключением к 5ka API")
    
@app.post("/telegram")
async def telegram_webhook(update: dict):
    telegram_update = Update.model_validate(update)
    await dp.feed_update(bot, telegram_update)
    return {"ok": True}

# === ПОДКЛЮЧЕНИЕ РОУТЕРОВ ===
app.include_router(api_router)