const API_BASE_URL = "https://fiveka-web-app.onrender.com";

// Основная функция для запросов
async function makeRequest(endpoint, method = "GET", body = null) {
    const options = {
        method,
        headers: {
            "Content-Type": "application/json",
        },
    };

    if (body) {
        options.body = JSON.stringify(body);
    }

    const response = await fetch(`${API_BASE_URL}${endpoint}`, options);
    
    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || `Ошибка: ${response.status}`);
    }

    return await response.json();
}

// Проверка доставки
async function checkDelivery(lat, lon) {
    try {
        // 1. Получаем магазины
        const storesData = await makeRequest("/api/stores", "POST", { lat, lon });
        if (!storesData.results || storesData.results.length === 0) {
            throw new Error("Нет магазинов в этой области");
        }

        const store = storesData.results[0];
        
        // 2. Получаем категории
        const categoriesData = await makeRequest("/api/categories");
        
        return {
            address: store.address,
            store: store,
            categories: categoriesData
        };
        
    } catch (error) {
        console.error("Ошибка проверки доставки:", error);
        throw error;
    }
}

// Обработчик кнопки
async function handleDeliveryCheck() {
    const button = document.getElementById("checkDeliveryBtn");
    const statusElem = document.getElementById("status");
    
    try {
        button.disabled = true;
        button.textContent = "Поиск...";
        
        // Получаем координаты с карты
        const coords = map.getCenter();
        const lat = coords[0];
        const lon = coords[1];
        
        // Проверяем доставку
        const result = await checkDelivery(lat, lon);
        
        // Сохраняем данные
        localStorage.setItem('deliveryData', JSON.stringify({
            address: result.address,
            storeId: result.store.sap_code,
            categories: result.categories
        }));
        
        // Показываем адрес
        document.getElementById("address").textContent = result.address;
        
        // Переходим в каталог
        window.location.href = "catalog.html";
        
    } catch (error) {
        console.error("Ошибка:", error);
        if (statusElem) {
            statusElem.textContent = error.message;
        }
    } finally {
        button.disabled = false;
        button.textContent = "Доставить сюда";
    }
}

// Инициализация
document.addEventListener("DOMContentLoaded", () => {
    const button = document.getElementById("checkDeliveryBtn");
    if (button) {
        button.addEventListener("click", handleDeliveryCheck);
    }
    
    // Восстанавливаем адрес если есть
    const savedData = localStorage.getItem('deliveryData');
    if (savedData) {
        const { address } = JSON.parse(savedData);
        document.getElementById("address").textContent = address;
    }
});