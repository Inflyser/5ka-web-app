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

# async def get_delivery_store(lat: float, lon: float):
#     async with httpx.AsyncClient() as client:
#         response = await client.get(
#             f"https://some-api.com/check-delivery?lat={lat}&lon={lon}"
#         )
    
#     if response.status_code != 200:
#         raise HTTPException(status_code=500, detail="Ошибка при запросе зоны доставки")

#     try:
#         data = response.json()
#     except ValueError:
#         raise HTTPException(status_code=500, detail="Невалидный JSON от API")

#     if not data.get("delivery_available"):
#         raise HTTPException(status_code=404, detail="Доставка в эту зону недоступна")

#     return {
#         "delivery_point": data.get("address"),
#         "store_id": data.get("store_id"),
#         "store_name": data.get("store_name"),
#     }
    
@app.get("/check-delivery")
async def check_delivery(lat: float, lon: float):
    url = "https://api.5ka.ru/api/v2/delivery_zone/check"
    payload = {"lat": lat, "lon": lon}

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload)

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Ошибка API Пятерочки")

    data = response.json()
    
    if not data.get("available"):
        raise HTTPException(status_code=404, detail="Доставка в эту зону недоступна")

    return {
        "store_id": data.get("store_id"),
        "region_id": data.get("region_id"),
        "delivery_type": data.get("delivery_type"),
        "address": data.get("address"),  # если есть
    }


# Получение товаров из магазина
@app.get("/store-items")
async def store_items(store_id: int = Query(...)):
    url = f"https://5ka.ru/api/v2/special_offers/?store={store_id}"
    async with httpx.AsyncClient() as client:
        r = await client.get(url)
        data = r.json()
    return data.get("results", [])



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