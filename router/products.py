from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()

flat_products = []  # Здесь будем хранить обработанные продукты

def process_products(raw_products: dict) -> dict:
    # Основная информация о категории
    category_info = {
        "category_id": raw_products["parent_id"],
        "category_name": raw_products["name"],
        "filters": raw_products["filters"]  # Можно дополнительно обработать фильтры
    }
    
    # Обрабатываем каждый продукт
    processed_products = []
    for product in raw_products["products"]:
        # Основные данные продукта
        processed_product = {
            "id": product["plu"],
            "name": product["name"],
            "image": product["image_links"]["normal"][0] if product["image_links"]["normal"] else None,
            "price": float(product["prices"]["regular"]),
            "discount_price": float(product["prices"]["discount"]) if product["prices"]["discount"] else None,
            "unit": product["property_clarification"] or product["uom"],
            "rating": product["rating"]["rating_average"],
            "reviews_count": product["rating"]["rates_count"],
            "in_stock": float(product["stock_limit"]) > 0 if product.get("stock_limit") else True,
            "badges": product.get("badges", []),
            "is_discount": product["prices"]["discount"] is not None
        }
        processed_products.append(processed_product)
    
    # Сортируем по наличию скидки и рейтингу
    processed_products.sort(
        key=lambda x: (
            -x["is_discount"],  
            -x["rating"]       
        )
    )
    
    return {
        **category_info,
        "products": processed_products,
        "products_count": len(processed_products)
    }

@router.get("/products")
async def get_products():
    return JSONResponse(content=flat_products)