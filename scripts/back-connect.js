async function getNearestStore(lat, lon) {
    const res = await fetch(`https://fiveka-web-app.onrender.com/nearest-store?lat=${lat}&lon=${lon}`);
    const data = await res.json();
    return data;
}

async function getStoreItems(storeId) {
    const res = await fetch(`https://fiveka-web-app.onrender.com/store-items?store_id=${storeId}`);
    const data = await res.json();
    return data;
}

async function loadData() {
    const coords = await getUserLocation(); // Например, через navigator.geolocation
    const store = await getNearestStore(coords.lat, coords.lon);
    
    if (store.id) {
        const items = await getStoreItems(store.id);
        renderItems(items); // твоя функция рендера товаров на фронте
    } else {
        alert("Магазин не найден");
    }
}