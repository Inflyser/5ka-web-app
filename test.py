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

    # Настройки прокси (пример)
    proxy = 'http://tl-85a86a8ebc70066fa6c97c81acd72f2b9a06dedcca4addf6e9b2395ce556bd41-country-ru-session-23424:ce35zon73c4c@proxy.toolip.io:31111'

    async with AsyncSession(impersonate="chrome120", verify=False) as session:
        try:
            # Обновляем заголовки сессии
            session.headers.update(headers)
            
            response = await session.get(
                url,
                params=params,
                proxy=proxy  # Добавляем прокси здесь
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