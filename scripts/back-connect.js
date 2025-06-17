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


// Получить адрес по координатам
async function getAddressByCoords(lat, lon) {
    const res = await fetch(`https://api.5ka.ru/api/v2/geo/address?lat=${lat}&lon=${lon}`);
    const data = await res.json();
    return data.address || "Адрес не найден";
}


// Загрузка данных при клике
async function handleDeliveryCheck() {
    try {
        const coords = map.getCenter();
        const address = await getAddressByCoords(coords.lat, coords.lon);

        // Отображаем адрес
        document.getElementById("address").textContent = "Ваш адрес: " + address;

        const deliveryResult = await checkDelivery(lat, lon);
        const { delivery, store_id, address: deliveryAddress } = deliveryResult;

        if (!delivery) {
            document.getElementById("status").textContent = "Доставка недоступна по вашему адресу.";
            return;
        }

        document.getElementById("status").textContent = `✅ Доставка доступна!\n🏪 Магазин ID: ${store_id}\n📍 Адрес доставки: ${deliveryAddress}`;

        // (Опционально) получить товары:
        const itemsRes = await fetch(`https://fiveka-web-app.onrender.com/store-items?store_id=${storeId}`);
        const items = await itemsRes.json();
        console.log("Товары магазина:", items);

    } catch (error) {
        console.error("Ошибка:", error.message);
        document.getElementById("status").textContent = "Доставка недоступна по вашему адресу.";
    }
}

// Привязка к кнопке
document.addEventListener("DOMContentLoaded", () => {
    const button = document.getElementById("checkDeliveryBtn");
    if (button) {
        button.addEventListener("click", handleDeliveryCheck);
    }
});

