import ssl
import aiohttp
import asyncio
from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import logging
from pyaterochka_api import Pyaterochka

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
FRONTEND_URL = "https://5ka-front.netlify.app"
WEBHOOK_URL = "https://fiveka-web-app.onrender.com/telegram"

proxy_str = os.getenv("HTTP_PROXY")  # или вставь строку напрямую

# --- SSL Context для aiohttp и monkey-patch ClientSession ---
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

original_session = aiohttp.ClientSession

class PatchedSession(aiohttp.ClientSession):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("connector", aiohttp.TCPConnector(ssl=ssl_context))
        super().__init__(*args, **kwargs)

aiohttp.ClientSession = PatchedSession  # monkey-patch

# --- FastAPI ---
app = FastAPI()

api_router = APIRouter()

class Location(BaseModel):
    lat: float
    lon: float

# Глобальная переменная для API Pyaterochka
pyaterochka_api: Pyaterochka | None = None

# lifespan — запуск и закрытие Pyaterochka один раз на старте/выходе
@asynccontextmanager
async def lifespan(app: FastAPI):
    global pyaterochka_api
    logger.info("Запускаем Pyaterochka API...")
    pyaterochka_api = await Pyaterochka(
        proxy=proxy_str,
        debug=False,  # выключи для скорости
        autoclose_browser=False,
        trust_env=False
    ).__aenter__()
    logger.info("Pyaterochka API запущен.")

    # Здесь можно добавить await bot.set_webhook(WEBHOOK_URL), если нужен бот

    yield

    logger.info("Закрываем Pyaterochka API...")
    await pyaterochka_api.__aexit__(None, None, None)
    logger.info("Pyaterochka API закрыт.")

app.router.lifespan_context = lifespan

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@api_router.post("/check-delivery")
async def check_delivery(loc: Location):
    if pyaterochka_api is None:
        raise HTTPException(status_code=503, detail="Сервис временно недоступен")

    logger.info(f"Получены координаты: lat={loc.lat}, lon={loc.lon}")

    try:
        result = await pyaterochka_api.find_store(longitude=loc.lon, latitude=loc.lat)
        logger.info(f"Результат поиска магазина: {result}")
        return {"status": "ok", "store": result}
    except Exception as e:
        logger.error(f"Ошибка при поиске магазина: {e}")
        raise HTTPException(status_code=500, detail="Ошибка при поиске магазина")

app.include_router(api_router)

# Простой health-check
@app.get("/ping")
async def ping():
    return JSONResponse(content={"status": "ok", "message": "Backend is alive!"})