from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from aiogram import Router, Dispatcher, Bot
from aiogram.types import Message, WebAppInfo
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.client.default import DefaultBotProperties
from aiogram.exceptions import TelegramForbiddenError
from aiogram.types import Update

import os
import httpx
import logging

from contextlib import asynccontextmanager
from dotenv import load_dotenv

from pydantic import BaseModel

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



def webapp_builder() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Click", web_app=WebAppInfo(
        url="https://5ka-front.netlify.app/index.html"), # Replace with your web app URL
        )  
    
    return builder.as_markup()

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    try:
        await message.answer(
            "Starting - Bot correct!",
            reply_markup=webapp_builder()
        )
    except TelegramForbiddenError:
        print(f"Пользователь {message.from_user.id} заблокировал бота.")
        

bot = Bot(
    BOT_TOKEN,
    # session=AiohttpSession(proxy="socks5://user:pass@host:port"),
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

dp = Dispatcher()
dp.include_router(router)
    
@asynccontextmanager
async def lifespan(app: FastAPI):
    await bot.set_webhook("https://fiveka-web-app.onrender.com/telegram")
    yield
    

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://5ka-front.netlify.app"],  # https://5ka-front.netlify.app
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/ping")
async def ping():
    return JSONResponse(content={"status": "ok", "message": "Backend is alive!"})


import httpx
from fastapi import HTTPException
from fastapi import APIRouter

class Location(BaseModel):
    lat: float
    lon: float

router = APIRouter()


@router.post("/check-delivery")
async def check_delivery(loc: Location):
    logger.info(f"Получены координаты: lat={loc.lat}, lon={loc.lon}")
    store_url = f"https://5d.5ka.ru/api/orders/v1/orders/stores/?lon={loc.lon}&lat={loc.lat}"

    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Referer": "https://5ka.ru/",
        "Origin": "https://5ka.ru"
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(store_url, headers=HEADERS)
            response.raise_for_status()
        except httpx.HTTPError as e:
            logger.error(f"Ошибка HTTP при запросе к API магазина: {e}")
            return {"success": False, "message": "Ошибка запроса к магазину"}

    try:
        stores_data = response.json()
        if not stores_data:
            logger.info("Нет магазинов рядом.")
            return {"success": False, "message": "Нет магазинов рядом"}

        store = stores_data[0]
        store_id = store.get("store_id")
        address = store.get("address")

        if not store_id or not address:
            logger.error("Некорректный формат данных магазина.")
            return {"success": False, "message": "Ошибка в формате данных"}

        logger.info(f"Найден магазин: {store_id}, адрес: {address}")
        return {"success": True, "store_id": store_id, "address": address}

    except Exception as e:
        logger.error(f"Ошибка обработки ответа от API: {e}")
        return {"success": False, "message": "Ошибка обработки данных"}
    
    


@app.get("/store-items")
async def store_items(store_id: str = Query(...), page: int = 1):
    url = "https://5ka.ru/graphql"
    payload = {
        "operationName": "products",
        "variables": {"storeId": store_id, "page": page, "perPage": 20},
        "query": """
            query products($storeId: ID!, $page: Int!, $perPage: Int!) {
              store(id: $storeId) {
                products(page: $page, perPage: $perPage) {
                  items {
                    id
                    title
                    price
                    unit
                    imageUrl
                    available
                  }
                  pageInfo {
                    totalPages
                  }
                }
              }
            }
        """
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=payload)
        except Exception as e:
            logger.error(f"Ошибка запроса к каталогу: {e}")
            raise HTTPException(status_code=500, detail="Ошибка соединения с 5ka GraphQL")

    if response.status_code != 200:
        logger.warning(f"Неверный статус каталога: {response.status_code}")
        raise HTTPException(status_code=500, detail="Ошибка получения товаров")

    try:
        data = response.json()
        items = data.get("data", {}).get("store", {}).get("products", {}).get("items", [])
    except Exception as e:
        logger.error(f"Ошибка обработки JSON: {e}")
        items = []

    return items


@app.post("/telegram")
async def telegram_webhook(update: dict):
    telegram_update = Update.model_validate(update)
    await dp.feed_update(bot, telegram_update)
    return {"ok": True}


app.include_router(router)