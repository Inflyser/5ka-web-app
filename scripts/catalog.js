import { renderCategories } from './categories.js';
import { renderProducts } from './product.js';
import { getProducts } from './api.js';

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
      renderProducts(response); // Теперь response содержит уже data часть
    } catch (err) {
      console.error(err);
      productsList.innerHTML = `Ошибка: ${err.message}`;
    }
  });

  backBtn.addEventListener('click', () => {
    productsList.innerHTML = '';
    categoriesList.style.display = 'block';
    productsList.style.display = 'none';
    backBtn.style.display = 'none';
  });
}