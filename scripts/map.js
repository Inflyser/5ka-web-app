let map, centerMarker;

function searchAddress() {
    const query = document.getElementById('address-input').value;
    ymaps.geocode(query).then(function (res) {
        const firstGeoObject = res.geoObjects.get(0);
        if (firstGeoObject) {
            const coords = firstGeoObject.geometry.getCoordinates();
            map.setCenter(coords);
            centerMarker.geometry.setCoordinates(coords);
            document.getElementById('address').innerText = 'Адрес: ' + firstGeoObject.getAddressLine();
        } else {
            alert("Адрес не найден");
        }
    });
}


ymaps.ready(function () {
    // Создаём карту
    map = new ymaps.Map("map", {
        center: [55.751574, 37.573856],
        zoom: 16,
        controls: ['zoomControl', 'geolocationControl']
    });

    // Маркер в центре карты
    centerMarker = new ymaps.Placemark(map.getCenter(), {}, {
        preset: 'islands#redIcon',
        iconColor: '#ff0000'
    });
    map.geoObjects.add(centerMarker);

    // Отслеживание движения карты
    map.events.add('boundschange', function () {
        const coords = map.getCenter(); // [lat, lon]
        const lat = coords[0];
        const lon = coords[1];
        lastCoords = coords;

        centerMarker.geometry.setCoordinates(coords);

        if (debounceTimeout) clearTimeout(debounceTimeout);
        debounceTimeout = setTimeout(() => preloadStore(lat, lon), 1000);
    });
});