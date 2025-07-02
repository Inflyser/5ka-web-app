function renderProducts(productsData) {
    const container = document.getElementById('productsList');
    container.innerHTML = '';

    if (!productsData?.length) {
        container.innerHTML = '<p>Товары не найдены</p>';
        return;
    }

    productsData.forEach(product => {
        const productEl = document.createElement('div');
        productEl.className = 'product';
        productEl.innerHTML = `
            <img src="${product.image || 'placeholder.jpg'}" alt="${product.name}">
            <h3>${product.name}</h3>
            <p>${product.price} ₽</p>
            <button>В корзину</button>
        `;
        container.appendChild(productEl);
    });
}