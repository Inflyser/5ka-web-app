import asyncio
from curl_cffi.requests import AsyncSession
import json

async def fetch_pyaterochka_stores(lat: float, lon: float):
    url = "https://5d.5ka.ru/api/orders/v1/orders/stores/"
    params = {
        "lat": lat,
        "lon": lon
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "Referer": "https://5ka.ru/",
        "Origin": "https://5ka.ru",
    }

    async with AsyncSession(impersonate="chrome120") as session:
        try:
            response = await session.get(
                url,
                params=params,
                headers=headers
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Ошибка при запросе: {e}")
            return None

async def main():
    latitude = 52.95417364044243
    longitude = 36.09554340003643
    
    stores_data = await fetch_pyaterochka_stores(latitude, longitude)
    if stores_data:
        print("Успешно получены данные:")
        print(json.dumps(stores_data, indent=2, ensure_ascii=False))
    else:
        print("Не удалось получить данные")

if __name__ == "__main__":
    asyncio.run(main())
    
