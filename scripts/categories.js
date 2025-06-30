export function renderProducts(products) {
    const productsListElem = document.getElementById('productsList');
    productsListElem.innerHTML = '';

    if (!products || products.length === 0) {
        productsListElem.innerHTML = '<p>Товары не найдены</p>';
        return;
    }

    const grid = document.createElement('div');
    grid.className = 'products-grid';

    products.forEach(product => {
        const card = document.createElement('div');
        card.className = 'product-card';

        const img = document.createElement('img');
        img.className = 'product-image';
        img.src = product.image_link || '';
        img.alt = product.name;

        const name = document.createElement('div');
        name.className = 'product-name';
        name.textContent = product.name;

        card.appendChild(name);
        card.appendChild(img);

        grid.appendChild(card);
    });

    productsListElem.appendChild(grid);
}



// export function renderCategories(rawCategories, searchQuery = '', onCategoryClick) {
//     const listElem = document.getElementById('categoriesList');
//     listElem.innerHTML = '';

//     if (!rawCategories || rawCategories.length === 0) {
//         listElem.innerHTML = '<p>Категории не найдены</p>';
//         return;
//     }

//     rawCategories.forEach(parent => {
//         const matchedSubs = parent.categories.filter(sub =>
//             sub.name.toLowerCase().includes(searchQuery.toLowerCase())
//         );

//         if (matchedSubs.length === 0) return;

//         const categoryBlock = document.createElement('div');
//         categoryBlock.className = 'category-block';

//         const categoryTitle = document.createElement('div');
//         categoryTitle.className = 'category-title';
//         categoryTitle.textContent = parent.name || 'Без названия';

//         const subGrid = document.createElement('div');
//         subGrid.className = 'subcategory-grid';

//         matchedSubs.forEach(sub => {
//             const card = document.createElement('div');
//             card.className = 'subcategory-card';

//             const img = document.createElement('img');
//             img.className = 'subcategory-image';
//             img.src = sub.image_link;
//             img.alt = sub.name;

//             const name = document.createElement('div');
//             name.className = 'subcategory-name';
//             name.textContent = sub.name;

//             card.appendChild(name);
//             card.appendChild(img);

//             // 👉 Клик вызывает внешний обработчик
//             card.addEventListener('click', () => {
//                 onCategoryClick?.(sub.id);
//             });

//             subGrid.appendChild(card);
//         });

//         categoryBlock.appendChild(categoryTitle);
//         categoryBlock.appendChild(subGrid);
//         listElem.appendChild(categoryBlock);
//     });
// }

// document.addEventListener("DOMContentLoaded", () => {
//     const rawCategories = JSON.parse(localStorage.getItem('categories'));
//     console.log("📦 Категории из localStorage:", rawCategories);
//     renderCategories(rawCategories);
// });