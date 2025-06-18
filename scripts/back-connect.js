
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


async function handleDeliveryCheck() {
    try {
        const coords = map.getCenter(); // [lat, lon]
        const lat = coords[0];
        const lon = coords[1];

        console.log("📍 Проверка координат:", lat, lon);

        const deliveryResult = await checkDelivery(lat, lon);

        // ✅ Показываем адрес, полученный с бэкенда:
        const deliveryAddress = deliveryResult.address || "Адрес не определён";
        document.getElementById("address").textContent = "📍 Ваш адрес: " + deliveryAddress;

        if (!deliveryResult?.store_id) {
            document.getElementById("status").textContent = "❌ Доставка недоступна по вашему адресу.";
            return;
        }

        const storeId = deliveryResult.store_id;

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

