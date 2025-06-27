function renderProducts(products) {
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
        img.src = product.image_link || ''; // замените на поле с изображением, если другое
        img.alt = product.name;

        const name = document.createElement('div');
        name.className = 'product-name';
        name.textContent = product.name;

        // Можно добавить цену и описание, если есть

        card.appendChild(name);
        card.appendChild(img);

        grid.appendChild(card);
    });

    productsListElem.appendChild(grid);
}