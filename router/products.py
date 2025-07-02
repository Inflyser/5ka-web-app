from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from typing import List, Dict, Optional
import re

router = APIRouter()

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
            "category_id": raw_products.get("parent_id", ""),
            "category_name": raw_products.get("name", ""),
            "filters": raw_products.get("filters", [])
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
        
        processed_products.sort(
            key=lambda x: (-x["is_discount"], -x["rating"])
        )
        
        return {
            **category_info,
            "products": processed_products,
            "products_count": len(processed_products)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing products: {str(e)}")

@router.post("/update_products")
async def update_products(raw_products: dict):
    try:
        processed = process_products(raw_products)
        products_store.clear()
        products_store.extend(processed["products"])
        return {"status": "success", "count": len(products_store)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/products")
async def get_products(limit: int = 20, offset: int = 0):
    try:
        return {
            "products": products_store[offset:offset+limit],
            "total": len(products_store),
            "limit": limit,
            "offset": offset
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))