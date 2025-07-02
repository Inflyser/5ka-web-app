export function initCatalog() {
  // 1. Получаем данные из localStorage с проверкой
  const rawCategories = localStorage.getItem('categories');
  const storeId = localStorage.getItem('storeId');
  
  if (!rawCategories) {
    console.error('Категории не найдены в localStorage');
    return;
  }

  // 2. Получаем DOM-элементы
  const categoriesList = document.getElementById('categoriesList');
  const productsList = document.getElementById('productsList');
  const backBtn = document.getElementById('backBtn');

  if (!categoriesList || !productsList || !backBtn) {
    console.error('Не найдены необходимые DOM-элементы');
    return;
  }

  try {
    // 3. Парсим категории с обработкой ошибок
    const categories = JSON.parse(rawCategories);
    
    // 4. Рендерим категории (убедитесь, что renderCategories экспортируется правильно)
    renderCategories(categories, '', async (categoryId) => {
      // Переключение видимости блоков
      categoriesList.style.display = 'none';
      productsList.style.display = 'block';
      backBtn.style.display = 'block';
      productsList.innerHTML = 'Загрузка товаров...';
      
      if (!storeId) {
        productsList.innerHTML = 'Ошибка: store_id не найден';
        return;
      }
      
      try {
        const response = await getProducts(storeId, categoryId);
        
        if (!response || !response.products) {
          throw new Error('Неверный формат данных о товарах');
        }
        
        const productsData = {
          products: response.products,
          category_name: response.category_name || ''
        };
        
        renderProducts(productsData);
      } catch (err) {
        console.error('Ошибка загрузки товаров:', err);
        productsList.innerHTML = 'Ошибка при загрузке товаров. Попробуйте позже.';
      }
    });

    // 5. Обработчик кнопки "Назад"
    backBtn.addEventListener('click', () => {
      productsList.innerHTML = '';
      categoriesList.style.display = 'block';
      productsList.style.display = 'none';
      backBtn.style.display = 'none';
    });

  } catch (e) {
    console.error('Ошибка при обработке категорий:', e);
    categoriesList.innerHTML = 'Ошибка при загрузке категорий';
  }
}