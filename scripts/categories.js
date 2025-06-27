function renderCategories(rawCategories) {
    const listElem = document.getElementById('categoriesList');
    listElem.innerHTML = '';

    if (!rawCategories || rawCategories.length === 0) {
        listElem.innerHTML = '<p>Категории не найдены</p>';
        return;
    }

    rawCategories.forEach(parent => {
        const parentName = parent.name || 'Без названия';
        const parentId = parent.id;

        const categoryBlock = document.createElement('div');
        categoryBlock.className = 'category-block';

        const categoryTitle = document.createElement('div');
        categoryTitle.className = 'category-title';
        categoryTitle.textContent = parentName;

        const subGrid = document.createElement('div');
        subGrid.className = 'subcategory-grid';

        parent.categories.forEach(sub => {
            const card = document.createElement('div');
            card.className = 'subcategory-card';

            const img = document.createElement('img');
            img.className = 'subcategory-image';
            img.src = sub.image_link;
            img.alt = sub.name;

            const name = document.createElement('div');
            name.className = 'subcategory-name';
            name.textContent = sub.name;

            const id = document.createElement('div');
            id.className = 'subcategory-id';
            id.textContent = `ID: ${sub.id}`;

            card.appendChild(name);
            card.appendChild(img);
            // card.appendChild(id);

            subGrid.appendChild(card);
        });

        categoryBlock.appendChild(categoryTitle);
        categoryBlock.appendChild(subGrid);
        listElem.appendChild(categoryBlock);
    });
}

document.addEventListener("DOMContentLoaded", () => {
    const rawCategories = JSON.parse(localStorage.getItem('categories'));
    renderCategories(rawCategories);
});