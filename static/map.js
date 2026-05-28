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

    // Variables for routing
    let userLocation = null;
    let currentRoute = null;
    const restaurants = [];

    // Location: [Latitude, Longitude, Popup Text]
    const loc = [39.9564, -75.1887, "<b>Hello!</b><br>This is Drexel University."];

    const blueIcon = L.icon({
        iconUrl: 'static/images/dragonpinblue.png',
        iconSize: [95, 95]
    });

    const yellowIcon = L.icon({
        iconUrl: 'static/images/dragonpinyellow.png',
        iconSize: [95, 95]
    });

    const redIcon = L.icon({
        iconUrl: 'static/images/FoodTruck.png',
        iconSize: [55,55]
    });
    // Build graph from OSRM route nodes (only connect adjacent waypoints)
    function buildGraph(coords) {
        const graph = {};
        for (let i = 0; i < coords.length; i++) {
            graph[i] = [];
            // Only connect to adjacent nodes to follow the actual road path
            if (i > 0) {
                const dist = haversineDistance(coords[i], coords[i - 1]);
                graph[i].push({ node: i - 1, distance: dist });
            }
            if (i < coords.length - 1) {
                const dist = haversineDistance(coords[i], coords[i + 1]);
                graph[i].push({ node: i + 1, distance: dist });
            }
        }
        return graph;
    }

    // Haversine distance formula
    function haversineDistance(coord1, coord2) {
        const R = 6371; // Earth's radius in km
        const lat1 = coord1[0] * Math.PI / 180;
        const lat2 = coord2[0] * Math.PI / 180;
        const dLat = (coord2[0] - coord1[0]) * Math.PI / 180;
        const dLon = (coord2[1] - coord1[1]) * Math.PI / 180;
        const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
                  Math.cos(lat1) * Math.cos(lat2) * Math.sin(dLon / 2) * Math.sin(dLon / 2);
        const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
        return R * c;
    }

    // Dijkstra's algorithm
    function dijkstra(graph, start, end, coords) {
        const distances = {};
        const previous = {};
        const unvisited = new Set();

        Object.keys(graph).forEach(node => {
            distances[node] = Infinity;
            previous[node] = null;
            unvisited.add(parseInt(node));
        });
        distances[start] = 0;

        while (unvisited.size > 0) {
            let current = null;
            let minDist = Infinity;

            unvisited.forEach(node => {
                if (distances[node] < minDist) {
                    minDist = distances[node];
                    current = node;
                }
            });

            if (current === null || distances[current] === Infinity) break;

            unvisited.delete(current);

            graph[current].forEach(neighbor => {
                if (unvisited.has(neighbor.node)) {
                    const alt = distances[current] + neighbor.distance;
                    if (alt < distances[neighbor.node]) {
                        distances[neighbor.node] = alt;
                        previous[neighbor.node] = current;
                    }
                }
            });
        }

        // Reconstruct path
        const path = [];
        let current = end;
        while (current !== null) {
            path.unshift(coords[current]);
            current = previous[current];
        }
        return path;
    }

    // Fetch route from OSRM and draw it
    function showOSRMRoute(start, end) {
        if (!userLocation) {
            alert("Please allow location access to show route");
            return;
        }

        const url = `https://router.project-osrm.org/route/v1/foot/${start[1]},${start[0]};${end[1]},${end[0]}?steps=true&geometries=geojson&overview=full`;

        fetch(url)
            .then(response => response.json())
            .then(data => {
                if (data.routes && data.routes.length > 0) {
                    const route = data.routes[0];
                    const coords = route.geometry.coordinates.map(c => [c[1], c[0]]); // Convert to [lat, lng]

                    // Build graph from route coordinates
                    const graph = buildGraph(coords);

                    // Run Dijkstra's algorithm
                    const path = dijkstra(graph, 0, coords.length - 1, coords);

                    // Draw the route
                    drawRoute(path);
                } else {
                    alert("No route found");
                }
            })
            .catch(error => {
                console.error("Error fetching OSRM route:", error);
                alert("Error fetching route");
            });
    }

    // Draw route on map
    function drawRoute(coords) {
        if (currentRoute) {
            map.removeLayer(currentRoute);
        }

        currentRoute = L.polyline(coords, {
            color: 'red',
            weight: 5,
            opacity: 0.8,
            dashArray: '10, 5'
        }).addTo(map);

        const bounds = L.latLngBounds(coords);
        map.fitBounds(bounds.pad(0.15));
    }
    // Add a single marker
    const marker = L.marker([loc[0], loc[1]], { icon: blueIcon }).addTo(map);
    marker.bindPopup(loc[2]);
    marker.on('click', function() {
        restaurants.push({name: "Drexel University", coords: [loc[0], loc[1]]});
        showOSRMRoute([userLocation.lat, userLocation.lng], [loc[0], loc[1]]);
    });

    const tatakiMarker = L.marker([39.957586599999054, -75.19207226199879], { icon: blueIcon }).addTo(map);
    tatakiMarker.bindPopup("This is Tataki Sushi and Ramen.");
    tatakiMarker.on('click', function() {
        showOSRMRoute([userLocation.lat, userLocation.lng], [39.957586599999054, -75.19207226199879]);
    });

    const hanMarker = L.marker([39.95672897997564, -75.19710636677178], { icon: blueIcon }).addTo(map);
    hanMarker.bindPopup("This is Han Dynasty.");
    hanMarker.on('click', function() {
        showOSRMRoute([userLocation.lat, userLocation.lng], [39.95672897997564, -75.19710636677178]);
    });

    const chikMarker = L.marker([39.95892892006141, -75.19066655281112], { icon: blueIcon }).addTo(map);
    chikMarker.bindPopup("This is Chik-fil-A.");
    chikMarker.on('click', function() {
        showOSRMRoute([userLocation.lat, userLocation.lng], [39.95892892006141, -75.19066655281112]);
    });

    const wildBlueMarker = L.marker([39.95892579555406, -75.19051829394947], { icon: blueIcon }).addTo(map);
    wildBlueMarker.bindPopup("This is Wild Blue Sushi.");
    wildBlueMarker.on('click', function() {
        showOSRMRoute([userLocation.lat, userLocation.lng], [39.95892579555406, -75.19051829394947]);
    });

    const chipotleMarker = L.marker([39.957211125669666, -75.19139423385867], { icon: blueIcon }).addTo(map);
    chipotleMarker.bindPopup("This is Chipotle.");
    chipotleMarker.on('click', function() {
        showOSRMRoute([userLocation.lat, userLocation.lng], [39.957211125669666, -75.19139423385867]);
    });

    const sabrinaMarker = L.marker([39.959963231800494, -75.19071384179624], { icon: blueIcon }).addTo(map);
    sabrinaMarker.bindPopup("This is Sabrina's.");
    sabrinaMarker.on('click', function() {
        showOSRMRoute([userLocation.lat, userLocation.lng], [39.959963231800494, -75.19071384179624]);
    });

    const mangomangomarker = L.marker([39.959262, -75.194584], { icon: yellowIcon }).addTo(map);
    mangomangomarker.bindPopup("This is Mango Mango.");
    mangomangomarker.on('click', function() {
        showOSRMRoute([userLocation.lat, userLocation.lng], [39.959262, -75.194584]);
    });

    const carvelMarker = L.marker([39.957404, -75.191870], { icon: yellowIcon }).addTo(map);
    carvelMarker.bindPopup("This is Carvel.");
    carvelMarker.on('click', function() {
        showOSRMRoute([userLocation.lat, userLocation.lng], [39.957404, -75.191870]);
    });
    const kiwiyogurtMarker = L.marker([39.954571, -75.195189], { icon: yellowIcon }).addTo(map);
    kiwiyogurtMarker.bindPopup("This is Kiwi Yogurt.");
    kiwiyogurtMarker.on('click', function() {
        showOSRMRoute([userLocation.lat, userLocation.lng], [39.954571, -75.195189]);
    });
    const surrealMarker = L.marker([39.9529, -75.1800], { icon: yellowIcon }).addTo(map);
    surrealMarker.bindPopup("This is Surreal Creamery. ");
    surrealMarker.on('click', function() {
        showOSRMRoute([userLocation.lat, userLocation.lng], [39.9529, -75.1800]);
    });

    const cocoMarker = L.marker([39.959559, -75.195166], { icon: yellowIcon }).addTo(map);
    cocoMarker.bindPopup("This is Coco's Creamery.");
    cocoMarker.on('click', function() {
        showOSRMRoute([userLocation.lat, userLocation.lng], [39.959559, -75.195166]);
    }
    );
    const maisonMarker = L.marker([39.953219, -75.183309], { icon: yellowIcon }).addTo(map);
    maisonMarker.bindPopup("This is Maison Sweet.");
    maisonMarker.on('click', function() {
        showOSRMRoute([userLocation.lat, userLocation.lng], [39.953219, -75.183309]);
    }
    );
    const insomniaMarker = L.marker([39.957366, -75.191708], { icon: yellowIcon }).addTo(map);
    insomniaMarker.bindPopup("This is Insomnia Cookies.");
    insomniaMarker.on('click', function() {
        showOSRMRoute([userLocation.lat, userLocation.lng], [39.957366, -75.191708]);
    });

    const happysunshine = L.marker([39.957597, -75.189485], { icon: redIcon }).addTo(map);
    happysunshine.bindPopup("This is Happy Sunshine.");
    happysunshine.on('click', function() {
        showOSRMRoute([userLocation.lat, userLocation.lng], [39.957597, -75.189485]);
    });

    const KC = L.marker([39.956946, -75.189365], { icon: redIcon }).addTo(map);
    KC.bindPopup("This is KC\'s Fresh Fruit Smoothies.");
    KC.on('click', function() {
        showOSRMRoute([userLocation.lat, userLocation.lng], [39.956946, -75.189365]);
    });

    const zapata = L.marker([39.954326, -75.185816], { icon: redIcon }).addTo(map);
    zapata.bindPopup("This is Zapata Food Truck.");
    zapata.on('click', function() {
        showOSRMRoute([userLocation.lat, userLocation.lng], [39.954326, -75.185816]);
    });

    const nanu = L.marker([39.956134, -75.189492], { icon: redIcon }).addTo(map);
    nanu.bindPopup("This is Nanu\'s Food Truck.");
    nanu.on('click', function() {
        showOSRMRoute([userLocation.lat, userLocation.lng], [39.956134, -75.189492]);
    });

    const megaM = L.marker([39.956016, -75.189523], { icon: redIcon }).addTo(map);
    megaM.bindPopup("This is Mega Food Truck.");
    megaM.on('click', function() {
        showOSRMRoute([userLocation.lat, userLocation.lng], [39.956016, -75.189523]);
    });

    const kami = L.marker([39.955254, -75.189680], { icon: redIcon }).addTo(map);
    kami.bindPopup("This is Kami\'s Korean Food Truck.");
    kami.on('click', function() {
        showOSRMRoute([userLocation.lat, userLocation.lng], [39.955254, -75.189680]);
    });


    map.locate({ setView: true, maxZoom: 16 });

    map.on('locationfound', function (e) {
        userLocation = e.latlng;  // Store user location for routing
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
