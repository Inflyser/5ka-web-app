export function renderCategories(data, searchQuery = '', onCategoryClick) {
    const container = document.getElementById('categoriesList');
    if (!container) return;
    
    // Деструктуризация с значениями по умолчанию
    const { categories = [] } = data || {};
    
    container.innerHTML = categories.length ? '' : '<p>Категории не найдены</p>';
    
    categories.forEach(category => {
        const filteredSubcategories = category.categories?.filter(sub => 
            sub.name?.toLowerCase().includes(searchQuery.toLowerCase())
        ) || [];
        
        if (!filteredSubcategories.length) return;
        
        container.innerHTML += `
            <div class="category-block">
                <h3>${category.name || 'Без названия'}</h3>
                <div class="subcategory-grid">
                    ${filteredSubcategories.map(sub => `
                        <div class="subcategory-card" data-id="${sub.id}">
                            <img src="${sub.image_link || 'placeholder.jpg'}" alt="${sub.name}">
                            <p>${sub.name}</p>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
    });

    // Делегирование событий
    container.addEventListener('click', (e) => {
        const card = e.target.closest('.subcategory-card');
        if (card) {
            onCategoryClick?.(card.dataset.id);
        }
    });
}

// Инициализация
document.addEventListener("DOMContentLoaded", () => {
    const rawData = JSON.parse(localStorage.getItem('storeData')) || {};
    renderCategories(rawData);
});