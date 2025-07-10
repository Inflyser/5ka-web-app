import asyncio
from curl_cffi.requests import AsyncSession
from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
import random
import json
import time

# Генерация случайных User-Agent
def get_random_user_agent():
    chrome_versions = [
        "120.0.0.0", "121.0.0.0", "122.0.0.0", 
        "123.0.0.0", "124.0.0.0", "125.0.0.0"
    ]
    return f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.choice(chrome_versions)} Safari/537.36"

async def fetch_pyaterochka_stores(lat: float, lon: float):
    url = "https://5d.5ka.ru/api/orders/v1/orders/stores/"
    params = {
        "lat": lat,
        "lon": lon,
        "_": str(int(time.time() * 1000))
    }
    
    headers = {
        "User-Agent": get_random_user_agent(),
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "Referer": "https://5ka.ru/",
        "Origin": "https://5ka.ru",
        "Sec-Ch-Ua": '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Windows"',
    }

    proxies = {
        "http": "http://tl-85a86a8ebc70066fa6c97c81acd72f2b9a06dedcca4addf6e9b2395ce556bd41-country-ru-session-001334:ce35zon73c4c@proxy.toolip.io:31111",
        "https": "http://tl-85a86a8ebc70066fa6c97c81acd72f2b9a06dedcca4addf6e9b2395ce556bd41-country-ru-session-001245:ce35zon73c4c@proxy.toolip.io:31111"
    }

    await asyncio.sleep(random.uniform(0.5, 1.5))

    async with AsyncSession(
        impersonate="chrome120",
        timeout=30,
        verify=False
    ) as session:
        response = await session.get(
            url,
            params=params,
            headers=headers,
            proxies=proxies,
        )
        
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"API returned status code {response.status_code}"
            )
        
        try:
            data = response.json()
            if not data:
                raise ValueError("Empty response from API")
            return data
        except json.JSONDecodeError:
            raise HTTPException(
                status_code=500,
                detail="Invalid JSON response from API"
            )

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Автоматический запрос при старте приложения
    print("- Запрашиваем данные Пятерочки...")
    try:
        result = await fetch_pyaterochka_stores(52.95417364044243, 36.09554340003643)
        print("✅ Данные успешно получены:", json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"❌ Ошибка: {str(e)}")
    yield  # Здесь приложение работает
    # Код для завершения (если нужно)

app = FastAPI(lifespan=lifespan)

@app.get("/get_stores")
async def get_stores(lat: float = 52.95417364044243, lon: float = 36.09554340003643):
    try:
        return await fetch_pyaterochka_stores(lat, lon)
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)