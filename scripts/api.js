export async function getProducts(store_id, category_id) {
    try {
        const response = await fetch("https://fiveka-web-app.onrender.com/get-products", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ store_id, category_id }),
        });

        if (!response.ok) {
            let errorMsg = "Ошибка при получении товаров";
            try {
                const errorData = await response.json();
                errorMsg = errorData.detail || errorData.message || errorMsg;
            } catch (e) {
                console.error("Не удалось разобрать ошибку:", e);
            }
            throw new Error(errorMsg);
        }

        const data = await response.json();
        
        // Проверка структуры ответа
        if (!data || data.status !== "ok" || !data.data) {
            throw new Error("Неверный формат данных от сервера");
        }
        
        return data;
        
    } catch (error) {
        console.error("Ошибка в getProducts:", error);
        throw error; // Перебрасываем ошибку дальше
    }
}