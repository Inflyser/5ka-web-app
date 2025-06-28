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

async function handleDeliveryCheck() {
    try {
        const coords = map.getCenter(); // [lat, lon]
        const lat = coords[0];
        const lon = coords[1];
        console.log("📍 Проверка координат:", lat, lon);

        // Сохраняем координаты
        localStorage.setItem('userCoords', JSON.stringify({ lat, lon }));

        const deliveryResult = await checkDelivery(lat, lon);
        const deliveryAddress = deliveryResult.address || "Адрес не определён";
        document.getElementById("address").textContent = "📍 Ваш адрес: " + deliveryAddress;

        if (deliveryResult && deliveryResult.categories) {
            // Сохраняем категории
            localStorage.setItem('categories', JSON.stringify(deliveryResult.categories));

            // Переходим на страницу с выбором категории
            window.location.href = 'h5.html';
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
console.log("✅ Скрипт back-connect.js загружен");

const checkDeliveryBtn = document.getElementById("checkDeliveryBtn");
if (checkDeliveryBtn) {
    console.log("✅ Кнопка найдена");
    checkDeliveryBtn.addEventListener("click", handleDeliveryCheck);
} else {
    console.error("❌ Кнопка checkDeliveryBtn не найдена");
}



// // Отдельная функция для получения товаров по категории и магазину
// export async function getProducts(store_id, category_id) {
//     const response = await fetch("https://fiveka-web-app.onrender.com/get-products", {
//         method: "POST",
//         headers: {
//             "Content-Type": "application/json",
//         },
//         body: JSON.stringify({ store_id, category_id }),
//     });

//     if (!response.ok) {
//         const error = await response.json();
//         throw new Error(error.detail || "Ошибка при получении товаров");
//     }

//     return await response.json();
// }
