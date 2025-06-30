export function renderCategories(rawCategories, searchQuery = '', onCategoryClick) {
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

        const categoryBlock = document.createElement('div');
        categoryBlock.className = 'category-block';

        const categoryTitle = document.createElement('div');
        categoryTitle.className = 'category-title';
        categoryTitle.textContent = parent.name || 'Без названия';

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

            // 👉 Клик вызывает внешний обработчик
            card.addEventListener('click', () => {
                onCategoryClick?.(sub.id);
            });

            subGrid.appendChild(card);
        });

        categoryBlock.appendChild(categoryTitle);
        categoryBlock.appendChild(subGrid);
        listElem.appendChild(categoryBlock);
    });
}

document.addEventListener("DOMContentLoaded", () => {
    const rawCategories = JSON.parse(localStorage.getItem('categories'));
    console.log("📦 Категории из localStorage:", rawCategories);
    renderCategories(rawCategories);
});