export function renderProducts(productsData) {
    const productsListElem = document.getElementById('productsList');
    productsListElem.innerHTML = '';

    if (!productsData || !productsData.products || productsData.products.length === 0) {
        productsListElem.innerHTML = '<p>Товары не найдены</p>';
        return;
    }

    const grid = document.createElement('div');
    grid.className = 'products-grid';

    productsData.products.forEach(product => {
        const card = document.createElement('div');
        card.className = 'product-card';
        
        // Бейдж скидки (безопасная проверка)
        if (product.is_discount && product.discount_price && product.price) {
            const discountPercent = Math.round((1 - product.discount_price/product.price)*100);
            const discountBadge = document.createElement('div');
            discountBadge.className = 'product-discount-badge';
            discountBadge.textContent = `${discountPercent}% от ${product.step || 1} шт`;
            card.appendChild(discountBadge);
        }

        // Рейтинг (с проверкой)
        const rating = document.createElement('div');
        rating.className = 'product-rating';
        rating.textContent = product.rating ? product.rating.toFixed(1) : '—';
        card.appendChild(rating);

        // Название товара
        const name = document.createElement('div');
        name.className = 'product-name';
        name.textContent = product.name || 'Без названия';
        card.appendChild(name);

        // Вес/объем (с проверкой)
        if (product.unit) {
            const unit = document.createElement('div');
            unit.className = 'product-unit';
            unit.textContent = product.unit;
            card.appendChild(unit);
        }

        // Цена и кнопка (с проверкой)
        const priceWrapper = document.createElement('div');
        priceWrapper.className = 'product-price-wrapper';
        
        const priceValue = product.discount_price || product.price;
        if (priceValue) {
            const price = document.createElement('div');
            price.className = 'product-price';
            price.textContent = `${priceValue}₽`;
            priceWrapper.appendChild(price);
        }
        
        const addButton = document.createElement('button');
        addButton.className = 'product-add-button';
        addButton.textContent = 'В корзину';
        priceWrapper.appendChild(addButton);
        
        card.appendChild(priceWrapper);

        // Бейдж "Комбо" (только если category_name существует)
        if (productsData.category_name && typeof productsData.category_name === 'string' && 
            productsData.category_name.includes('Готовые блюда')) {
            const comboBadge = document.createElement('div');
            comboBadge.className = 'product-combo-badge';
            comboBadge.textContent = 'Комбо';
            card.appendChild(comboBadge);
        }

        grid.appendChild(card);
    });

    productsListElem.appendChild(grid);
}