export function renderProducts(productsData) {
    const productsListElem = document.getElementById('productsList');
    productsListElem.innerHTML = '';

    if (!productsData || !productsData.products || productsData.products.length === 0) {
        productsListElem.innerHTML = '<p>Товары не найдены</p>';
        return;
    }

    // Создаем сетку для товаров
    const grid = document.createElement('div');
    grid.className = 'products-grid';

    productsData.products.forEach(product => {
        const card = document.createElement('div');
        card.className = 'product-card';
        
        // Бейдж скидки (если есть)
        if (product.is_discount) {
            const discountBadge = document.createElement('div');
            discountBadge.className = 'product-discount-badge';
            discountBadge.textContent = `${Math.round((1 - product.discount_price/product.price)*100)}% от ${product.step || 1} шт`;
            card.appendChild(discountBadge);
        }

        // Рейтинг
        const rating = document.createElement('div');
        rating.className = 'product-rating';
        rating.textContent = product.rating ? product.rating.toFixed(1) : '—';
        card.appendChild(rating);

        // Название товара
        const name = document.createElement('div');
        name.className = 'product-name';
        name.textContent = product.name;
        card.appendChild(name);

        // Вес/объем
        if (product.unit) {
            const unit = document.createElement('div');
            unit.className = 'product-unit';
            unit.textContent = product.unit;
            card.appendChild(unit);
        }

        // Цена и кнопка
        const priceWrapper = document.createElement('div');
        priceWrapper.className = 'product-price-wrapper';
        
        const price = document.createElement('div');
        price.className = 'product-price';
        price.textContent = `${product.discount_price || product.price}₽`;
        priceWrapper.appendChild(price);
        
        const addButton = document.createElement('button');
        addButton.className = 'product-add-button';
        addButton.textContent = 'В корзину';
        priceWrapper.appendChild(addButton);
        
        card.appendChild(priceWrapper);

        // Бейдж "Комбо" (пример для определенных категорий)
        if (product.category_name.includes('Готовые блюда')) {
            const comboBadge = document.createElement('div');
            comboBadge.className = 'product-combo-badge';
            comboBadge.textContent = 'Комбо';
            card.appendChild(comboBadge);
        }

        grid.appendChild(card);
    });

    productsListElem.appendChild(grid);
}