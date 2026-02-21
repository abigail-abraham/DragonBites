try {
    // Initialize the map and set its view (latitude, longitude, zoom level)
    const map = L.map('map').setView([39.9564, -75.1887], 13);

    // Add OpenStreetMap tiles
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        maxZoom: 19
    }).addTo(map);

    // Add Search Bar (Geocoder)
    L.Control.geocoder().addTo(map);

    // Location: [Latitude, Longitude, Popup Text]
    const loc = [39.9564, -75.1887, "<b>Hello!</b><br>This is Drexel University."];

    const blueIcon = L.icon({
        iconUrl: 'static/dragonpinblue.png',
        iconSize: [95, 95]
    });

    const yellowIcon = L.icon({
        iconUrl: 'static/dragonpinyellow.png',
        iconSize: [95, 95]
    });
    // Add a single marker
    const marker = L.marker([loc[0], loc[1]], { icon: blueIcon }).addTo(map);
    marker.bindPopup(loc[2]);

    marker.on('click', function (e) {
        console.log("Marker clicked at", e.latlng);

    });

    map.locate({ setView: true, maxZoom: 16 });

    map.on('locationfound', function (e) {
        const radius = e.accuracy / 2;
        const current = L.marker(e.latlng, { icon: yellowIcon }).addTo(map);
        current.bindPopup("You are here!").openPopup();
        L.circle(e.latlng, radius).addTo(map);


    })
    map.on('locationerror', function (e) {
        alert("Could not find your location");
    })

} catch (error) {
    console.error("Error initializing the map:", error);
}
