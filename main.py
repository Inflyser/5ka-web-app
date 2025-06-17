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

from contextlib import asynccontextmanager
from dotenv import load_dotenv

from pydantic import BaseModel

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")


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
    allow_origins=["*"],  # https://5ka-front.netlify.app
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/ping")
async def ping():
    return JSONResponse(content={"status": "ok", "message": "Backend is alive!"})


import httpx
from fastapi import HTTPException

class Location(BaseModel):
    lat: float
    lon: float

@app.post("/check-delivery")
async def check_delivery(loc: Location):
    url = "https://5ka.ru/graphql"

    payload = {
        "operationName": "deliveryZones",
        "variables": {"lat": loc.lat, "lon": loc.lon},
        "query": """
            query deliveryZones($lat: Float!, $lon: Float!) {
              deliveryZones(lat: $lat, lon: $lon) {
                storeId
                available
                deliveryType
                address
              }
            }
        """
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload)

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Ошибка GraphQL запроса")

    data = response.json()
    zones = data.get("data", {}).get("deliveryZones", [])

    for zone in zones:
        if zone.get("available"):
            return {
                "delivery": True,
                "store_id": zone.get("storeId"),
                "delivery_type": zone.get("deliveryType"),
                "address": zone.get("address")
            }

    raise HTTPException(status_code=404, detail="Доставка в эту зону недоступна")

# Получение товаров из магазина
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
        response = await client.post(url, json=payload)

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Ошибка получения товаров")

    data = response.json()
    items = data.get("data", {}).get("store", {}).get("products", {}).get("items", [])
    return items



@app.post("/telegram")
async def telegram_webhook(update: dict):
    telegram_update = Update.model_validate(update)
    await dp.feed_update(bot, telegram_update)
    return {"ok": True}


# # Получение ближайшего магазина
# @app.get("/nearest-store")
# async def nearest_store(lat: float = Query(...), lon: float = Query(...)):
#     url = f"https://5ka.ru/api/v2/stores/?latitude={lat}&longitude={lon}"
#     async with httpx.AsyncClient() as client:
#         r = await client.get(url)
#         data = r.json()
#     if data.get("results"):
#         store = data["results"][0]
#         return {
#             "id": store.get("id"),
#             "address": store.get("address"),
#             "store": store
#         }
#     return {"error": "Store not found"}