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

    store_url = (
        f"https://5d.5ka.ru/api/orders/v1/orders/stores/?lon={loc.lon}&lat={loc.lat}"
    )

    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "Referer": "https://5ka.ru/",
        "Origin": "https://5ka.ru",
        "Connection": "keep-alive",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Host": "5d.5ka.ru",
        "X-Requested-With": "XMLHttpRequest",
        "Cookie": "spid=1749845165342_d9758ee051d22005b531d79bc8a52ce9_6rxd6xewi00r4vup; _ym_uid=1749845167776844367; _ym_d=1749845167; _ga=GA1.1.955548613.1749847022; tmr_lvid=24326f0c87c187980b45074a326a3e14; tmr_lvidTS=1749847022146; _ga_YJHF8Y9KXK=GS2.1.s1749847022$o1$g1$t1749847686$j60$l0$h0; SRV=73886aee-6a12-46c9-9c9d-5a6f809da3ee; TS018c7dc5=01a2d8bbf4934280e4b867096c8382807313aad58545132e1cc75381ee0d2809503447bd33f1e77d931ebe2da7ce4dada153bc68dcf3233bbaa3fe7bd1185233b321e74e07; spjs=1750422682127_095ae855_0134ff91_ddfa1d600b5aed12a82eb698304eae6c_ccgcjLeP8yPehzn4GowCqrwSnTcCSn8P39KngtYEjYg0bZFxe/Yve0K/TKzo1MXFYRq+O06jR6D+CqqoNP17AUwFyehxyy2M3JFz04JOr+oOKfBgWOA5WvOepoa/wNHBQEk9PW/S5qfTqHtrlk7xAF0WLz9HnzOpyNV1cNFfzt46c+ciDJRoWbCoEofLJ/670Cm8WVmx5bZCuk//Dnxg1Tkl2WlmvvJGv/Ih1PAsqM0sZ9G1EMo4Pteem5KuwagPodpHxo0FsTQh2N7vm8WCMrZBTBwkypdj3pY6C5f5+tnN4dUlo87+T5oSN/SYQDz/IFuV14uGi3Tg+d3d+ENxEdRMaK7VybW0aNQ9n8N6RlLOB4HgNDyofyqSB5ZzRRiptAy3VAujbg5Gf2zc6aHFxHJJPewYAtTDX5Zq6p5OAHFdBLhqE8hfe6wU1tay6SwMDyjhtjuXWn7y3+XFzWPQgAIq6Dj7FCAV8K5tD5dKUbLeBJkcYlqWaSz0B0ZGPwtbL8bmYClAXdwA35Flq8PeXoKc6b66dpDSk30ueL9p5UUaJ8rqBM1QgciysMFlnKyrXkXXYBYPKl1BapDSHmTYX0ILtqaN9WBgRHzfGhuWglKmcX05wPj1BytTaj+SDZmvXaPFVQKabj/Lw3DA3FWpiXUu8iIP51s0wKw+6TnRVZLSi91MNKwxItwmOsngOmZGGvTAVLKpbb86g9fgsKTomCXtsIFu1io6N588uxtHVtIUXovaXjd8A88zTBxgOzfzWZJeWvtLZk7DoiVlHuf0ZHhesGE+VtppxY0w8Zaz5QUTgH5PmcNVFMCYOUtXzvOiX4W7aRZMcy/YgzVG0sn8rV0AsOQc4tuIFg+w4czE6qnWioxvSUJyJdUJOeyd76SEDdOfPBXL8Sfcg7Zvk1r2LkoItXUhxQw59k+SNskS315TXkS27PVB0aOqGsrI4IeGhkEtHYGM/u4yescXa7QAX0imJsfhQX3d0wCya5+08irUrKenCiI/EeWcOLxNRtMzhx+b/Tav+yIvjsmYRU7+RB5Tu2EmiPYtKom0ZTD3eipWj2JiFcaLKNaG3/u3gueHEqnbin5WMrXOpztK8Fsmpwoi6kgSYz8+WqMUoee+CtqeXbf1+PSYK1FoVHTY1+U29k6qim0FJyZUbV9/09rgYFrg3f1QWGIrrddQEbR/r6h8RTZnLMQoKNQNNmKeR/urd1g8LYjGMLL33wuvrAzgsVhhj5lAPnMn27HEsmBIPKoZNfZ2Alpc7qHZFlQJB/zfAyjEorumAXD2PKqvu0aSwkYRnVgQjXRCW8YLawcIjIwIQfB1R+oOSr7mFfDM1HN6Ra0xcQzUaDfDmypIWsPkhFGAY4dX/n07QDYoYZ1D/1CtIrfurDF+/NF4viQRz/OkWP5Dwr1JsrS/s19uluLUhp7pgi0lwEkj4McH6qTI8oE9hIloIktrJ9rHOhWE6FwsWQ+y4xzGeKnTrZA+lvuD5gVs3so/TXqwhYHUFwnhcYeOBbxNU=; spsc=1750422682127_4132f08d446c3e6d07604dd6f77e7edf_P-zmhvTtThCB6.cUeF1EG4I56mOsVjDWbStjhueC0L2LKHSXnZXuKJfWFFGTHJ45Z; TS01658276=01a2d8bbf4b1ce8924888067285641ea5b92c449c4659fec79e83ac1c4e432d13917181f8881f8a9c7df56ecfeb8a8e7446c6a1b512fd2c134677ae74cae2a3e8f4627c68f313252b1364f60652e05b9efe77a58b0; _ym_isad=2; _ym_visorc=b"
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