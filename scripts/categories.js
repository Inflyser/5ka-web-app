import { getProducts } from './back-connect.js';

function renderCategories(rawCategories, searchQuery = '') {
    const listElem = document.getElementById('categoriesList');
    listElem.innerHTML = '';

    if (!rawCategories || rawCategories.length === 0) {
        listElem.innerHTML = '<p>Категории не найдены</p>';
        return;
    }

    rawCategories.forEach(parent => {
        // Фильтруем подкатегории по поиску
        const matchedSubs = parent.categories.filter(sub =>
            sub.name.toLowerCase().includes(searchQuery.toLowerCase())
        );

        if (matchedSubs.length === 0) return;

        const parentName = parent.name || 'Без названия';

        const categoryBlock = document.createElement('div');
        categoryBlock.className = 'category-block';

        const categoryTitle = document.createElement('div');
        categoryTitle.className = 'category-title';
        categoryTitle.textContent = parentName;

        const subGrid = document.createElement('div');
        subGrid.className = 'subcategory-grid';

        matchedSubs.forEach(sub => {
            const card = document.createElement('div');
            card.className = 'subcategory-card';

            const img = document.createElement('img');
            img.className = 'subcategory-image';
            img.src = sub.image_link || '';
            img.alt = sub.name;

            const name = document.createElement('div');
            name.className = 'subcategory-name';
            name.textContent = sub.name;

            // Текст сверху, картинка снизу
            card.appendChild(name);
            card.appendChild(img);

            // Обработчик клика по категории
            card.addEventListener('click', async () => {
                const storeObj = JSON.parse(localStorage.getItem('store'));
                const storeId = storeObj?.store_id;
                const categoryId = sub.id;

                if (!storeId || !categoryId) {
                    console.error('store_id или category_id не найдены');
                    alert('Ошибка: данные магазина или категории отсутствуют.');
                    return;
                }

                try {
                    // Получаем товары с бэкенда
                    const data = await getProducts(storeId, categoryId);

                    if (!data.products || data.products.length === 0) {
                        alert('Товары для выбранной категории не найдены.');
                        return;
                    }

                    // Сохраняем выбранную категорию и товары для дальнейшего использования
                    localStorage.setItem('selected_category', JSON.stringify(sub));
                    localStorage.setItem('products', JSON.stringify(data.products));

                    // Переходим на страницу продуктов
                    window.location.href = 'products.html';

                } catch (error) {
                    console.error('Ошибка при запросе товаров:', error);
                    alert('Не удалось получить товары. Попробуйте позже.');
                }
            });

            subGrid.appendChild(card);
        });

        categoryBlock.appendChild(categoryTitle);
        categoryBlock.appendChild(subGrid);
        listElem.appendChild(categoryBlock);
    });
}

document.addEventListener("DOMContentLoaded", () => {
    const rawCategories = JSON.parse(localStorage.getItem('categories')) || [];
    renderCategories(rawCategories);

    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            const query = e.target.value.trim();
            renderCategories(rawCategories, query);
        });
    }
});