export function renderProducts(productsData) {
    const productsListElem = document.getElementById('productsList');
    productsListElem.innerHTML = '';

    if (!productsData?.products?.length) {
        productsListElem.innerHTML = '<p>Товары не найдены</p>';
        return;
    }

    const grid = document.createElement('div');
    grid.className = 'products-grid';

    productsData.products.forEach(product => {
        const card = document.createElement('div');
        card.className = 'product-card';
        
        // Изображение товара
        if (product.image) {
            const img = document.createElement('img');
            img.src = product.image;
            img.alt = product.name;
            img.className = 'product-image';
            card.appendChild(img);
        }

        // Бейдж скидки
        if (product.discount_price) {
            const discountPercent = Math.round(
                (1 - product.discount_price / product.price) * 100
            );
            const discountBadge = document.createElement('div');
            discountBadge.className = 'product-discount-badge';
            discountBadge.textContent = `-${discountPercent}%`;
            card.appendChild(discountBadge);
        }

        // Название товара
        const name = document.createElement('h3');
        name.className = 'product-name';
        name.textContent = product.name || 'Без названия';
        card.appendChild(name);

        // Вес/объем
        if (product.unit) {
            const unit = document.createElement('div');
            unit.className = 'product-unit';
            unit.textContent = product.unit;
            card.appendChild(unit);
        }

        // Цены
        const priceWrapper = document.createElement('div');
        priceWrapper.className = 'product-price-wrapper';
        
        if (product.discount_price) {
            const oldPrice = document.createElement('span');
            oldPrice.className = 'product-old-price';
            oldPrice.textContent = `${product.price}₽`;
            priceWrapper.appendChild(oldPrice);
        }

        const price = document.createElement('div');
        price.className = 'product-price';
        price.textContent = `${(product.discount_price || product.price)}₽`;
        priceWrapper.appendChild(price);
        
        card.appendChild(priceWrapper);

        // Кнопка добавления
        const addButton = document.createElement('button');
        addButton.className = 'product-add-button';
        addButton.textContent = product.in_stock ? 'В корзину' : 'Нет в наличии';
        addButton.disabled = !product.in_stock;
        card.appendChild(addButton);

        grid.appendChild(card);
    });

    productsListElem.appendChild(grid);
}