document.querySelector('.apply-btn').addEventListener('click', function (e) {
    e.preventDefault();

    // Get all checked filters
    const checkboxes = document.querySelectorAll('#filters-form input[name="filter"]:checked');
    const filters = Array.from(checkboxes).map(cb => cb.value);

    // Get price range
    const minPrice = document.querySelector('#min-price').value;
    const maxPrice = document.querySelector('#max-price').value;

    // Send AJAX request
    fetch('/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ filters: filters, minPrice: minPrice, maxPrice: maxPrice })
    })
        .then(response => response.json())
        .then(data => {
            // Update the restaurants list
            const contentArea = document.querySelector('.content-area');
            let html = '<h2>Food listing</h2>';
            if (data.restaurants.length === 0) {
                html += '<p>No restaurants match your filters.</p>';
            } else {
                data.restaurants.forEach(restaurant => {
                    html += `<p>${restaurant[0]}</p>`;
                });
            }
            contentArea.innerHTML = html;
        })
        .catch(error => console.error('Error:', error));
});