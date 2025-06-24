from fastapi import APIRouter
from fastapi.responses import JSONResponse
import json

router = APIRouter()

def flatten_categories(raw_categories: list) -> list:
    result = []
    for parent in raw_categories:
        parent_name = parent.get("name")
        for sub in parent.get("categories", []):
            icons = {icon["type"]: icon["url"] for icon in sub.get("additional_icons", [])}
            result.append({
                "id": sub["id"],
                "name": sub["name"],
                "image": sub["image_link"],
                "gradient": [sub["gradient_start"], sub["gradient_end"]],
                "title_color": sub["title_color"],
                "icons": icons,
                "parent_name": parent_name
            })
    return result

# Загружаешь JSON с категориями (путь к файлу укажи свой)
with open("your_raw_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

flat_categories = flatten_categories(data["categories"])

@router.get("/categories")
async def get_categories():
    return JSONResponse(content=flat_categories)