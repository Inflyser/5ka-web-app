function renderCategories(categories, searchQuery = '', onSelect) {
    const container = document.getElementById('categoriesList');
    container.innerHTML = '';

    categories.forEach(category => {
        const categoryEl = document.createElement('div');
        categoryEl.className = 'category';
        categoryEl.innerHTML = `
            <h3>${category.name}</h3>
            <div class="subcategories"></div>
        `;
        
        const subContainer = categoryEl.querySelector('.subcategories');
        
        category.categories.forEach(sub => {
            const subEl = document.createElement('div');
            subEl.className = 'subcategory';
            subEl.innerHTML = `
                <img src="${sub.image_link}" alt="${sub.name}">
                <p>${sub.name}</p>
            `;
            subEl.addEventListener('click', () => onSelect(sub.id));
            subContainer.appendChild(subEl);
        });
        
        container.appendChild(categoryEl);
    });
}