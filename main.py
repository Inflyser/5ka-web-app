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
        url="https://5ka-front.netlify.app/index"), # Replace with your web app URL
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
    allow_origins=["*"],  # https://inflyser.github.io
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/ping")
async def ping():
    return JSONResponse(content={"status": "ok", "message": "Backend is alive!"})


# Получение ближайшего магазина
@app.get("/nearest-store")
async def nearest_store(lat: float = Query(...), lon: float = Query(...)):
    url = f"https://5ka.ru/api/v2/stores/?latitude={lat}&longitude={lon}"
    async with httpx.AsyncClient() as client:
        r = await client.get(url)
        data = r.json()
    if data.get("results"):
        store = data["results"][0]
        return {
            "id": store.get("id"),
            "address": store.get("address"),
            "store": store
        }
    return {"error": "Store not found"}

# Получение товаров из магазина
@app.get("/store-items")
async def store_items(store_id: int = Query(...)):
    url = f"https://5ka.ru/api/v2/special_offers/?store={store_id}"
    async with httpx.AsyncClient() as client:
        r = await client.get(url)
        data = r.json()
    return data.get("results", [])