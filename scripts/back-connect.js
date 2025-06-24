
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
    return await response.json();
}

async function handleDeliveryCheck() {
    try {
        const coords = map.getCenter(); // [lat, lon]
        const lat = coords[0];
        const lon = coords[1];
        console.log("📍 Проверка координат:", lat, lon);
        const deliveryResult = await checkDelivery(lat, lon);
        const deliveryAddress = deliveryResult.address || "Адрес не определён";
        document.getElementById("address").textContent = "📍 Ваш адрес: " + deliveryAddress;
        if (deliveryResult && deliveryResult.categories) {
            // Сохраняем категории в localStorage
            localStorage.setItem('categories', JSON.stringify(deliveryResult.categories));
            // Переходим на страницу h5.html
            window.location.href = 'page/h5.html';
            return;
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

document.addEventListener("DOMContentLoaded", () => {
    const button = document.getElementById("checkDeliveryBtn");
    if (button) {
        button.addEventListener("click", handleDeliveryCheck);
    }
});