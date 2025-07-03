from curl_cffi import requests
import json
import re
from typing import Optional, Dict, List
import time
from urllib.parse import urljoin

class DynamicPyaterochkaAPI:
    def __init__(self):
        self.base_url = "https://5ka.ru"
        self.api_version = self._detect_api_version()
        self.session = requests.Session()
        self._init_session()
        self.last_request_time = 0
        self.request_delay = 1.5  # Задержка между запросами

    def _detect_api_version(self) -> str:
        """Автоматическое определение актуальной версии API"""
        try:
            response = requests.get(self.base_url, impersonate="chrome110")
            # Ищем версию API в JavaScript коде страницы
            match = re.search(r'apiVersion:\s*["\'](v\d+)["\']', response.text)
            return match.group(1) if match else "v3"
        except:
            return "v3"

    def _init_session(self):
        """Динамическая инициализация сессии с заголовками"""
        self.session.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "X-Requested-With": "XMLHttpRequest",
        }
        self.session.verify = False

    def _get_dynamic_headers(self) -> Dict:
        """Генерация динамических заголовков для каждого запроса"""
        return {
            "X-Timestamp": str(int(time.time())),
            "X-Client": "web_dynamic_parser",
            "X-Api-Version": self.api_version,
        }

    def _rate_limit(self):
        """Контроль частоты запросов"""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.request_delay:
            time.sleep(self.request_delay - elapsed)
        self.last_request_time = time.time()

    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Optional[Dict]:
        """Умный запрос с автоматической адаптацией"""
        self._rate_limit()
        
        url = urljoin(self.base_url, f"/api/{self.api_version}/{endpoint}")
        headers = {**self.session.headers, **self._get_dynamic_headers()}
        
        try:
            response = self.session.get(
                url,
                params=params or {},
                headers=headers,
                impersonate="chrome110"
            )
            
            # Автоматическое обновление API версии при 404
            if response.status_code == 404:
                self.api_version = self._detect_api_version()
                return self._make_request(endpoint, params)
                
            response.raise_for_status()
            return response.json()
            
        except requests.RequestsError as e:
            print(f"Request failed: {e}")
            return None

    def smart_store_search(self, lat: float, lon: float) -> Optional[Dict]:
        """Умный поиск магазина с автоматическим выбором endpoint"""
        endpoints = [
            f"stores/?lat={lat}&lon={lon}",
            f"orders/stores/?lat={lat}&lon={lon}",
            f"shops/?lat={lat}&lon={lon}"
        ]
        
        for endpoint in endpoints:
            result = self._make_request(endpoint)
            if result and isinstance(result, list) and len(result) > 0:
                return result[0]
            elif result and isinstance(result, dict) and 'results' in result:
                return result['results'][0] if result['results'] else None
                
        return None

    def smart_get_products(self, store_id: str, category_id: str) -> Optional[List[Dict]]:
        """Адаптивный метод получения товаров"""
        params = {
            "store_id": store_id,
            "category_id": category_id,
            "mode": "delivery",
            "limit": 100
        }
        
        # Пробуем разные варианты endpoints
        endpoints = [
            "products/",
            "items/",
            "goods/"
        ]
        
        for endpoint in endpoints:
            result = self._make_request(endpoint, params)
            if result:
                return result
                
        return None

# Пример использования в FastAPI роутерах
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

router = APIRouter()

def get_api():
    return DynamicPyaterochkaAPI()

class Location(BaseModel):
    lat: float
    lon: float

@router.post("/dynamic/stores")
def find_store(loc: Location, api: DynamicPyaterochkaAPI = Depends(get_api)):
    store = api.smart_store_search(loc.lat, loc.lon)
    if not store:
        raise HTTPException(404, "Магазин не найден")
    return store

@router.get("/dynamic/products/{store_id}/{category_id}")
def get_products(store_id: str, category_id: str, api: DynamicPyaterochkaAPI = Depends(get_api)):
    products = api.smart_get_products(store_id, category_id)
    if not products:
        raise HTTPException(404, "Товары не найдены")
    return products