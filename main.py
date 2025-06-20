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
        "x-app-version": "0.1.1.dev",
        "x-device-id": "afc296b4-0312-461f-98cd-e1755c4ed629",
        "x-platform": "webapp",
        "origin": "https://5ka.ru",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cookie": "spid=1749845165342_d9758ee051d22005b531d79bc8a52ce9_6rxd6xewi00r4vup; _ym_uid=1749845167776844367; _ym_d=1749845167; _ga=GA1.1.955548613.1749847022; tmr_lvid=24326f0c87c187980b45074a326a3e14; tmr_lvidTS=1749847022146; _ga_YJHF8Y9KXK=GS2.1.s1749847022$o1$g1$t1749847686$j60$l0$h0; spjs=1750422682127_095ae855_0134ff91_ddfa1d600b5aed12a82eb698304eae6c_ccgcjLeP8yPehzn4GowCqrwSnTcCSn8P39KngtYEjYg0bZFxe/Yve0K/TKzo1MXFYRq+O06jR6D+CqqoNP17AUwFyehxyy2M3JFz04JOr+oOKfBgWOA5WvOepoa/wNHBQEk9PW/S5qfTqHtrlk7xAF0WLz9HnzOpyNV1cNFfzt46c+ciDJRoWbCoEofLJ/670Cm8WVmx5bZCuk//Dnxg1Tkl2WlmvvJGv/Ih1PAsqM0sZ9G1EMo4Pteem5KuwagPodpHxo0FsTQh2N7vm8WCMrZBTBwkypdj3pY6C5f5+tnN4dUlo87+T5oSN/SYQDz/IFuV14uGi3Tg+d3d+ENxEdRMaK7VybW0aNQ9n8N6RlLOB4HgNDyofyqSB5ZzRRiptAy3VAujbg5Gf2zc6aHFxHJJPewYAtTDX5Zq6p5OAHFdBLhqE8hfe6wU1tay6SwMDyjhtjuXWn7y3+XFzWPQgAIq6Dj7FCAV8K5tD5dKUbLeBJkcYlqWaSz0B0ZGPwtbL8bmYClAXdwA35Flq8PeXoKc6b66dpDSk30ueL9p5UUaJ8rqBM1QgciysMFlnKyrXkXXYBYPKl1BapDSHmTYX0ILtqaN9WBgRHzfGhuWglKmcX05wPj1BytTaj+SDZmvXaPFVQKabj/Lw3DA3FWpiXUu8iIP51s0wKw+6TnRVZLSi91MNKwxItwmOsngOmZGGvTAVLKpbb86g9fgsKTomCXtsIFu1io6N588uxtHVtIUXovaXjd8A88zTBxgOzfzWZJeWvtLZk7DoiVlHuf0ZHhesGE+VtppxY0w8Zaz5QUTgH5PmcNVFMCYOUtXzvOiX4W7aRZMcy/YgzVG0sn8rV0AsOQc4tuIFg+w4czE6qnWioxvSUJyJdUJOeyd76SEDdOfPBXL8Sfcg7Zvk1r2LkoItXUhxQw59k+SNskS315TXkS27PVB0aOqGsrI4IeGhkEtHYGM/u4yescXa7QAX0imJsfhQX3d0wCya5+08irUrKenCiI/EeWcOLxNRtMzhx+b/Tav+yIvjsmYRU7+RB5Tu2EmiPYtKom0ZTD3eipWj2JiFcaLKNaG3/u3gueHEqnbin5WMrXOpztK8Fsmpwoi6kgSYz8+WqMUoee+CtqeXbf1+PSYK1FoVHTY1+U29k6qim0FJyZUbV9/09rgYFrg3f1QWGIrrddQEbR/r6h8RTZnLMQoKNQNNmKeR/urd1g8LYjGMLL33wuvrAzgsVhhj5lAPnMn27HEsmBIPKoZNfZ2Alpc7qHZFlQJB/zfAyjEorumAXD2PKqvu0aSwkYRnVgQjXRCW8YLawcIjIwIQfB1R+oOSr7mFfDM1HN6Ra0xcQzUaDfDmypIWsPkhFGAY4dX/n07QDYoYZ1D/1CtIrfurDF+/NF4viQRz/OkWP5Dwr1JsrS/s19uluLUhp7pgi0lwEkj4McH6qTI8oE9hIloIktrJ9rHOhWE6FwsWQ+y4xzGeKnTrZA+lvuD5gVs3so/TXqwhYHUFwnhcYeOBbxNU=; _ym_isad=2; _ym_visorc=b; spsc=1750424166110_2c0e5234a886671660e4c8c177d93ca4_5AMa1g4VZcC0FTXLTHZPtUTZ.xBH63zeBzXgLL0xfKqsQe7bDKm9J4nAvOPOQ4sDZ; TS01658276=01a2d8bbf4bf88ad236f301b02a4e673c72b9f288c99dee7d5704ac6f5a06423619f71130137d6f794db38a923daefaa4ec260c54e80c11f00904637375693d587ce655194158ab0ee91439bf9927afa1554edfa85e8f437e1ce7092fd765c5b7bf7d8cc5a6439aeabf40ef0a5ff22b3112da767f3689aa72c9deb1f3c1e26e97e960e9ef5; SRV=6afdbacc-6b94-4763-978f-13d94a49f443; TS018c7dc5=01a2d8bbf4c2af8939ab070623938182b19e6f7749d1a7959c221718c398b8d4190d331f09ee594dd56ceacb3d1d40b78bb48428862cb0c2393af233ce445f0ab44f29423a"
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