export async function getProducts(store_id, category_id) {
    try {
        const response = await fetch("https://fiveka-web-app.onrender.com/get-products", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ 
                store_id: store_id,
                category_id: category_id 
            }),
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || "Ошибка при получении товаров");
        }

        const data = await response.json();
        
        if (data.status !== "success") {
            throw new Error("Неверный статус ответа");
        }
        
        return data.data; // Возвращаем только data часть
        
    } catch (error) {
        console.error("Ошибка в getProducts:", error);
        throw error;
    }
}