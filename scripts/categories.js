function renderCategories(rawCategories, searchQuery = '') {
    const listElem = document.getElementById('categoriesList');
    listElem.innerHTML = '';

    if (!rawCategories || rawCategories.length === 0) {
        listElem.innerHTML = '<p>Категории не найдены</p>';
        return;
    }

    rawCategories.forEach(parent => {
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
            img.src = sub.image_link;
            img.alt = sub.name;

            const name = document.createElement('div');
            name.className = 'subcategory-name';
            name.textContent = sub.name;

            card.appendChild(name);
            card.appendChild(img);

            // Добавляем обработчик клика для запроса товаров этой категории
            card.addEventListener('click', async () => {
                try {
                    // Отображаем индикатор загрузки, очистка списка товаров
                    const productsListElem = document.getElementById('productsList');
                    productsListElem.innerHTML = 'Загрузка товаров...';

                    // Получаем координаты из localStorage или другого источника (например, заранее сохранённые)
                    const coords = JSON.parse(localStorage.getItem('userCoords'));
                    if (!coords) {
                        productsListElem.innerHTML = 'Ошибка: координаты пользователя не найдены.';
                        return;
                    }

                    // Запрос на бек с координатами + category_id
                    const productsData = await fetchProducts(coords.lat, coords.lon, sub.id);
                    renderProducts(productsData.products);
                } catch (err) {
                    console.error(err);
                    document.getElementById('productsList').innerHTML = 'Ошибка при загрузке товаров.';
                }
            });

            subGrid.appendChild(card);
        });

        categoryBlock.appendChild(categoryTitle);
        categoryBlock.appendChild(subGrid);
        listElem.appendChild(categoryBlock);
    });
}