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

// Проверить доставку и получить категории и магазин
async function checkDelivery(lat, lon) {
    const response = await fetch("https://fiveka-web-app.onrender.com/get-store-and-categories", {
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

    return await response.json();
}

// Основная функция при клике на кнопку "Проверить доставку"
async function handleDeliveryCheck() {
    try {
        // Получаем координаты из карты
        const { lat, lng: lon } = map.getCenter();
        console.log("📍 Проверка координат:", lat, lon);

        // Сохраняем координаты
        localStorage.setItem('userCoords', JSON.stringify({ lat, lon }));

        // Отправляем координаты на сервер
        const deliveryResult = await checkDelivery(lat, lon);

        // Отображаем адрес
        const deliveryAddress = deliveryResult.address || "Адрес не определён";
        document.getElementById("address").textContent = "📍 Ваш адрес: " + deliveryAddress;

        if (!window.map || typeof map.getCenter !== 'function') {
            alert('Карта ещё не загрузилась');
            return;
        }
        // Сохраняем магазин и категории
        if (deliveryResult.store_id) {
            localStorage.setItem('store', JSON.stringify({ store_id: deliveryResult.store_id }));
        }

        if (deliveryResult.categories) {
            localStorage.setItem('categories', JSON.stringify(deliveryResult.categories));
            window.location.href = 'catalog.html'; // Переход на страницу выбора категории
        } else {
            document.getElementById("status").textContent = "❌ Категории не получены";
        }


    } catch (error) {
        console.error("Ошибка:", error);
        const statusElem = document.getElementById("status");
        if (statusElem) {
            statusElem.textContent = "⚠️ Ошибка при проверке доставки: " + error.message;
        }
    }
}

// Запуск после загрузки страницы
document.addEventListener("DOMContentLoaded", () => {
    const button = document.getElementById("checkDeliveryBtn");
    if (button) {
        button.addEventListener("click", handleDeliveryCheck);
    }
});

// Отдельная функция для получения товаров по категории и магазину
export async function getProducts(store_id, category_id) {
    const response = await fetch("https://fiveka-web-app.onrender.com/get-products", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ store_id, category_id }),
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || "Ошибка при получении товаров");
    }

    return await response.json();
}
