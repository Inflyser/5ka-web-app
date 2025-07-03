from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional
import re
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

# Временное хранилище (в production используйте БД)
products_store = []

def safe_float_conversion(value: Optional[str]) -> Optional[float]:
    if value is None:
        return None
    try:
        return float(re.sub(r'[^\d.]', '', value))
    except (ValueError, TypeError):
        return None

def process_products(raw_products: dict) -> dict:
    try:
        category_info = {
            "id": raw_products.get("parent_id", ""),
            "name": raw_products.get("name", ""),
            "store_id": raw_products.get("sap_code_store_id", "")
        }
        
        processed_products = []
        for product in raw_products.get("products", []):
            regular_price = safe_float_conversion(product.get("prices", {}).get("regular"))
            discount_price = safe_float_conversion(product.get("prices", {}).get("discount"))
            
            processed_product = {
                "id": product.get("plu"),
                "name": product.get("name"),
                "image": (product.get("image_links", {}).get("normal") or [None])[0],
                "price": regular_price,
                "discount_price": discount_price,
                "unit": product.get("property_clarification") or product.get("uom"),
                "rating": product.get("rating", {}).get("rating_average", 0),
                "reviews_count": product.get("rating", {}).get("rates_count", 0),
                "in_stock": safe_float_conversion(product.get("stock_limit", "0")) > 0,
                "badges": product.get("badges", []),
                "is_discount": discount_price is not None
            }
            processed_products.append(processed_product)
        
        # Сортировка: сначала товары со скидкой, затем по рейтингу
        processed_products.sort(key=lambda x: (-x["is_discount"], -x["rating"]))
        
        return {
            "category_info": category_info,
            "products": processed_products,
            "filters": raw_products.get("filters", []),
            "products_count": len(processed_products)
        }
    except Exception as e:
        logger.error(f"Error processing products: {str(e)}")
        raise