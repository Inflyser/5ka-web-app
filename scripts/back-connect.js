async function getUserLocation() {
    return new Promise((resolve, reject) => {
        navigator.geolocation.getCurrentPosition(
            (position) => {
                resolve({
                    lat: position.coords.latitude,
                    lon: position.coords.longitude
                });
            },
            (err) => {
                console.error("Геолокация не работает", err);
                alert("Геолокация недоступна");
                reject(err);
            }
        );
    });
}

async function getNearestStore(lat, lon) {
    try {
        const res = await fetch(`https://fiveka-web-app.onrender.com/nearest-store?lat=${lat}&lon=${lon}`);
        const data = await res.json();
        return data;
    } catch (err) {
        console.error("Ошибка при получении магазина:", err);
        return {};
    }
}

async function getStoreItems(storeId) {
    const res = await fetch(`https://fiveka-web-app.onrender.com/store-items?store_id=${storeId}`);
    const data = await res.json();
    return data;
}

async function loadData() {
    const coords = await getUserLocation();
    console.log("Координаты пользователя:", coords);

    const store = await getNearestStore(coords.lat, coords.lon);
    console.log("Ближайший магазин:", store);

    if (store.id) {
        const items = await getStoreItems(store.id);
        console.log("Товары магазина:", items);
        renderItems(items);
    } else {
        alert("Магазин не найден");
    }
}