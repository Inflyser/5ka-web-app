// Инициализация каталога
async function initCatalog() {
    const savedData = localStorage.getItem('deliveryData');
    if (!savedData) {
        window.location.href = "address.html";
        return;
    }

    const { storeId, categories } = JSON.parse(savedData);
    const categoriesList = document.getElementById('categoriesList');
    const productsList = document.getElementById('productsList');
    const backBtn = document.getElementById('backBtn');

    // Показываем категории
    renderCategories(categories, '', async (categoryId) => {
        categoriesList.style.display = 'none';
        productsList.style.display = 'block';
        backBtn.style.display = 'block';
        productsList.innerHTML = 'Загрузка...';
        
        try {
            const response = await fetch(`${API_BASE_URL}/api/products`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    store_id: storeId,
                    category_id: categoryId
                }),
            });
            
            const productsData = await response.json();
            renderProducts(productsData);
            
        } catch (error) {
            productsList.innerHTML = 'Ошибка загрузки товаров';
            console.error(error);
        }
    });

    // Кнопка "Назад"
    backBtn.addEventListener('click', () => {
        productsList.innerHTML = '';
        categoriesList.style.display = 'block';
        productsList.style.display = 'none';
        backBtn.style.display = 'none';
    });
}

// Запуск при загрузке
document.addEventListener('DOMContentLoaded', initCatalog);