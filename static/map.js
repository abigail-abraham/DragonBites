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

    const tatakiMarker = L.marker([39.957586599999054, -75.19207226199879], { icon: blueIcon }).addTo(map);
    tatakiMarker.bindPopup("This is Tataki Sushi and Ramen.");
    const hanMarker = L.marker([39.95672897997564, -75.19710636677178], { icon: blueIcon }).addTo(map);
    hanMarker.bindPopup("This is Han Dynasty.");
    const chikMarker = L.marker([39.95892892006141, -75.19066655281112], { icon: blueIcon }).addTo(map);
    chikMarker.bindPopup("This is Chik-fil-A.");
    const wildBlueMarker = L.marker([39.95892579555406, -75.19051829394947], { icon: blueIcon }).addTo(map);
    wildBlueMarker.bindPopup("This is Wild Blue Sushi.");
    const chipotleMarker = L.marker([39.957211125669666, -75.19139423385867], { icon: blueIcon }).addTo(map);
    chipotleMarker.bindPopup("This is Chipotle.");
    const sabrinaMarker = L.marker([39.959963231800494, -75.19071384179624], { icon: blueIcon }).addTo(map);
    sabrinaMarker.bindPopup("This is Sabrina's.");

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
