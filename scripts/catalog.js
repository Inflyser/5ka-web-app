export function initCatalog() {
  const rawCategories = JSON.parse(localStorage.getItem('categories'));
  const storeId = localStorage.getItem('storeId');
  
  const categoriesList = document.getElementById('categoriesList');
  const productsList = document.getElementById('productsList');
  const backBtn = document.getElementById('backBtn');

  renderCategories(rawCategories, '', async (categoryId) => {
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
      
      // Проверяем, что данные пришли в правильном формате
      if (!response || !response.products) {
        throw new Error('Неверный формат данных о товарах');
      }
      
      // Формируем объект, который ожидает renderProducts
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

  backBtn.addEventListener('click', () => {
    productsList.innerHTML = '';
    categoriesList.style.display = 'block';
    productsList.style.display = 'none';
    backBtn.style.display = 'none';
  });
}
