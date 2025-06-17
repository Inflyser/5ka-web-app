
// Получить координаты пользователя
async function getUserLocation() {
    return new Promise((resolve, reject) => {
        navigator.geolocation.getCurrentPosition(
            (position) => {
                resolve({
                    lat: position.coords.latitude,
                    lon: position.coords.longitude
                });
            },
            (err) => {
                console.error("Геолокация не работает", err);
                alert("Геолокация недоступна");
                reject(err);
            }
        );
    });
}

console.log("lat:", lat, "lon:", lon);

// Проверка доставки
async function checkDelivery(lat, lon) {
    const response = await fetch("https://fiveka-web-app.onrender.com/check-delivery", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ lat, lon }),
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || "Ошибка при проверке доставки");
    }

    return await response.json(); // { delivery, store_id, ... }
}


// Получить адрес по координатам
async function getAddressByCoords(lat, lon) {
    const res = await fetch(`https://api.5ka.ru/api/v2/geo/address?lat=${lat}&lon=${lon}`);
    const data = await res.json();
    return data.address || "Адрес не найден";
}


// Загрузка данных при клике
async function handleDeliveryCheck() {
    try {
        const coords = map.getCenter(); // [lat, lon]
        const lat = coords[0];
        const lon = coords[1];

        console.log("📍 Проверка координат:", lat, lon);

        const address = await getAddressByCoords(lat, lon);
        document.getElementById("address").textContent = "Ваш адрес: " + address;

        const deliveryResult = await checkDelivery(lat, lon);

        if (!deliveryResult?.store_id) {
            document.getElementById("status").textContent = "❌ Доставка недоступна по вашему адресу.";
            return;
        }

        const storeId = deliveryResult.store_id;
        const deliveryAddress = deliveryResult.address || "Адрес не указан";

        document.getElementById("status").textContent =
            `✅ Доставка доступна!\n🏪 Магазин ID: ${storeId}\n📍 Адрес доставки: ${deliveryAddress}`;

        const itemsRes = await fetch(`https://fiveka-web-app.onrender.com/store-items?store_id=${storeId}`);
        if (!itemsRes.ok) throw new Error("Не удалось загрузить товары");

        const items = await itemsRes.json();
        console.log("🛒 Товары магазина:", items);

    } catch (error) {
        console.error("Ошибка:", error);
        const statusElem = document.getElementById("status");
        if (statusElem) {
            statusElem.textContent = "⚠️ Ошибка при проверке доставки: " + error.message;
        }
    }
}

// Привязка к кнопке
document.addEventListener("DOMContentLoaded", () => {
    const button = document.getElementById("checkDeliveryBtn");
    if (button) {
        button.addEventListener("click", handleDeliveryCheck);
    }
});

