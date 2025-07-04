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
            
            // Добавляем градиентный фон и цвет текста
            if (sub.gradient && sub.gradient.length === 2) {
                const [startColor, endColor] = sub.gradient;
                card.style.background = `linear-gradient(135deg, ${startColor}, ${endColor})`;
                
                // Если есть цвет текста - применяем его
                if (sub.title_color) {
                    card.style.color = sub.title_color;
                }
            }

            const img = document.createElement('img');
            img.className = 'subcategory-image';
            img.src = sub.image_link || 'placeholder.png'; // fallback изображение
            img.alt = sub.name;
            img.onerror = () => { img.src = 'placeholder.png'; }; // обработчик ошибок загрузки

            const name = document.createElement('div');
            name.className = 'subcategory-name';
            name.textContent = sub.name;

            card.appendChild(name);
            card.appendChild(img);

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