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