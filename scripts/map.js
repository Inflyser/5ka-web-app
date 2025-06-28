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
    map = new ymaps.Map("map", {
        center: [55.751574, 37.573856],
        zoom: 16,
        controls: ['zoomControl', 'geolocationControl']
    });

    centerMarker = new ymaps.Placemark(map.getCenter(), {}, {
        preset: 'islands#redIcon',
        iconColor: '#ff0000'
    });
    map.geoObjects.add(centerMarker);

    map.events.add('boundschange', function () {
        const coords = map.getCenter();
        centerMarker.geometry.setCoordinates(coords);

        ymaps.geocode(coords).then(function (res) {
            const firstGeoObject = res.geoObjects.get(0);
            const address = firstGeoObject ? firstGeoObject.getAddressLine() : 'не найден';
            document.getElementById('address').innerText = 'Адрес: ' + address;
            document.getElementById('address-input').value = address;
        });
    });
});

window.map = map;