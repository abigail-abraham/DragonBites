// Food Truck Filter Functionality

document.addEventListener('DOMContentLoaded', function() {
    // Get filter elements
    const applyBtn = document.querySelector('.foodtruck-filter-apply');
    const clearBtn = document.querySelector('.foodtruck-filter-clear');
    const filterCheckboxes = document.querySelectorAll('.foodtruck-filter-label input[type="checkbox"]');
    const minPriceInput = document.querySelector('.price-inputs input[placeholder="Min $"]');
    const maxPriceInput = document.querySelector('.price-inputs input[placeholder="Max $"]');
    
    // Load all food trucks on page load
    loadAllFoodTrucks();
    
    // Apply filters button
    if (applyBtn) {
        applyBtn.addEventListener('click', applyFilters);
    }
    
    // Clear filters button
    if (clearBtn) {
        clearBtn.addEventListener('click', clearFilters);
    }
});

function applyFilters() {
    // Get all checked filters
    const checkboxes = document.querySelectorAll('.foodtruck-filter-label input[type="checkbox"]:checked');
    const filters = [];
    
    checkboxes.forEach(checkbox => {
        const value = checkbox.getAttribute('data-value');
        if (value) {
            filters.push(value);
        }
    });
    
    // Get price range
    const minPrice = document.querySelector('.price-inputs input[placeholder="Min $"]').value;
    const maxPrice = document.querySelector('.price-inputs input[placeholder="Max $"]').value;
    
    // Send AJAX request to filter API
    fetch('/api/filter-food-trucks', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            filters: filters,
            minPrice: minPrice ? parseFloat(minPrice) : null,
            maxPrice: maxPrice ? parseFloat(maxPrice) : null
        })
    })
    .then(response => response.json())
    .then(data => {
        updateFoodTruckGrid(data.foodTrucks);
    })
    .catch(error => console.error('Error filtering food trucks:', error));
}

function updateFoodTruckGrid(foodTrucks) {
    const grid = document.querySelector('.foodtruck-grid');
    
    if (foodTrucks.length === 0) {
        grid.innerHTML = '<p class="no-results">No food trucks match your filters. Try adjusting your selections.</p>';
        return;
    }
    
    // Map of food truck names to their emoji/icons for display
    const foodTruckIcons = {
        'Happy Sunshine': '☀️',
        'KC\'s Fresh Fruit Smoothie': '🍓',
        'Nanu\'s Hot Chicken': '🍗',
        'Mega Food Truck': '🚚',
        'Kami\'s Korean Food Truck': '🇰🇷',
        'Cucina Zapata': '🌮'
    };
    
    // Build HTML for filtered results
    let html = '';
    foodTrucks.forEach(truck => {
        const icon = foodTruckIcons[truck.name] || '🚚';
        html += `
            <div class="foodtruck-card" onclick="openModal('${truck.name.replace(/'/g, "\\'")}')">
                <h3>${icon} ${truck.name}</h3>
                <p class="price">$${truck.price.toFixed(2)}</p>
                <p class="rating">★ ${truck.rating.toFixed(1)}</p>
            </div>
        `;
    });
    
    grid.innerHTML = html;
}

function clearFilters() {
    // Uncheck all checkboxes
    const checkboxes = document.querySelectorAll('.foodtruck-filter-label input[type="checkbox"]');
    checkboxes.forEach(checkbox => {
        checkbox.checked = false;
    });
    
    // Clear price inputs
    document.querySelector('.price-inputs input[placeholder="Min $"]').value = '';
    document.querySelector('.price-inputs input[placeholder="Max $"]').value = '';
    
    // Show all food trucks
    showAllFoodTrucks();
}

function showAllFoodTrucks() {
    // Reset to show all food trucks by fetching with no filters
    fetch('/api/filter-food-trucks', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            filters: [],
            minPrice: null,
            maxPrice: null
        })
    })
    .then(response => response.json())
    .then(data => {
        updateFoodTruckGrid(data.foodTrucks);
    })
    .catch(error => console.error('Error loading food trucks:', error));
}

function loadAllFoodTrucks() {
    showAllFoodTrucks();
}
