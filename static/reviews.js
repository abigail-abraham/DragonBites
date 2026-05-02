// Reviews System/Section - Which lets users add, view, and delete reviews

// Turns a number (1-5) into star symbols
function displayStars(rating) {
    return '★'.repeat(rating) + '☆'.repeat(5 - rating);
}

// Fetches reviews from the database and ADDS them below hardcoded reviews
async function loadReviews(locationName, locationType) {
    try {
        const response = await fetch('/get_reviews', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({location_name: locationName, location_type: locationType})
        });
        const data = await response.json();
        const reviewsList = document.getElementById('reviews-list');
        if (!reviewsList) return;
        
        // Check if there are already hardcoded reviews in the list
        const hasHardcoded = reviewsList.children.length > 0;
        
        if (data.reviews.length === 0) {
            // No database reviews - nothing to add
            return;
        }
        
        // Add a separator if there are hardcoded reviews already showing
        let separatorAdded = false;
        
        // Append each database review
        data.reviews.forEach(review => {
            // Add separator before first database review if we have hardcoded reviews
            if (hasHardcoded && !separatorAdded) {
                const separator = document.createElement('div');
                separator.className = 'reviews-separator';
                separator.innerHTML = '<hr style="margin: 15px 0 10px 0;"><p style="margin: 5px 0 10px 0; font-weight: bold; color: #192841;">Recent Student Reviews:</p>';
                reviewsList.appendChild(separator);
                separatorAdded = true;
            }
            
            const reviewDiv = document.createElement('div');
            reviewDiv.className = 'review-item';
            reviewDiv.setAttribute('data-review-id', review.id);
            reviewDiv.innerHTML = `
                <div class="review-header">
                    <strong class="reviewer-name">${escapeHtml(review.author_name)}</strong>
                    <span class="review-stars">${displayStars(review.rating)}</span>
                    <span class="review-date">${escapeHtml(review.date)}</span>
                    <button class="delete-review-btn" onclick="deleteReview(${review.id})" title="Delete review">Delete</button>
                </div>
                <p class="review-comment">${escapeHtml(review.comment)}</p>
            `;
            reviewsList.appendChild(reviewDiv);
        });
    } catch (error) {
        console.error('Error loading reviews:', error);
    }
}

// Stops bad characters from breaking the page!!
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Deletes a review when user clicks the delete button
async function deleteReview(reviewId) {
    if (confirm('Are you sure you want to delete this review?')) {
        try {
            const response = await fetch('/delete_review', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({review_id: reviewId})
            });
            const data = await response.json();
            if (data.success) {
                alert('Review deleted successfully.');
                // Remove the review element from DOM directly
                const reviewElement = document.querySelector(`.review-item[data-review-id="${reviewId}"]`);
                if (reviewElement) reviewElement.remove();
            }
        } catch (error) {
            console.error('Error deleting review:', error);
            alert('Error deleting review. Please try again.');
        }
    }
}

// Opens the write a review form modal
function openReviewForm(locationName, locationType) {
    let modal = document.getElementById('reviewFormModal');
    if (!modal) {
        modal = document.createElement('div');
        modal.id = 'reviewFormModal';
        modal.className = 'modal';
        modal.innerHTML = `
            <div class="modal-content review-form-content">
                <span class="close-btn" onclick="closeReviewForm()">&times;</span>
                <h3>Write a Review</h3>
                <form id="reviewForm">
                    <div class="form-group">
                        <label>Your Name (optional)</label>
                        <input type="text" id="author_name" placeholder="Anonymous">
                    </div>
                    <div class="form-group">
                        <label>Rating</label>
                        <div class="star-rating">
                            <span data-rating="1">☆</span>
                            <span data-rating="2">☆</span>
                            <span data-rating="3">☆</span>
                            <span data-rating="4">☆</span>
                            <span data-rating="5">☆</span>
                        </div>
                        <input type="hidden" id="rating" required>
                    </div>
                    <div class="form-group">
                        <label>Your Review</label>
                        <textarea id="comment" rows="4" required placeholder="Share your experience..."></textarea>
                    </div>
                    <button type="submit" class="submit-review-btn">Submit Review</button>
                </form>
            </div>
        `;
        document.body.appendChild(modal);
        
        // Makes the stars clickable
        modal.querySelectorAll('.star-rating span').forEach(star => {
            star.onclick = () => {
                const rating = parseInt(star.getAttribute('data-rating'));
                document.getElementById('rating').value = rating;
                modal.querySelectorAll('.star-rating span').forEach((s, i) => {
                    s.innerHTML = i < rating ? '★' : '☆';
                });
            };
        });
        
        // Handles the form submission
        const form = modal.querySelector('#reviewForm');
        form.onsubmit = async (e) => {
            e.preventDefault();
            const rating = document.getElementById('rating').value;
            const comment = document.getElementById('comment').value;
            const author_name = document.getElementById('author_name').value;
            
            if (!rating) { alert('Please select a rating'); return; }
            if (!comment.trim()) { alert('Please write a review'); return; }
            
            const response = await fetch('/add_review', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    location_name: locationName,
                    location_type: locationType,
                    rating: parseInt(rating),
                    comment: comment,
                    author_name: author_name || 'Anonymous'
                })
            });
            const data = await response.json();
            if (data.success) {
                alert('Review added successfully.');
                closeReviewForm();
                
                // Remove any existing database reviews and separator
                const reviewsList = document.getElementById('reviews-list');
                if (reviewsList) {
                    const dbReviews = reviewsList.querySelectorAll('.review-item[data-review-id]');
                    dbReviews.forEach(el => el.remove());
                    const separator = reviewsList.querySelector('.reviews-separator');
                    if (separator) separator.remove();
                }
                
                // Load fresh database reviews (hardcoded ones stay because they don't have data-review-id)
                loadReviews(locationName, locationType);
            }
        };
    }
    window.currentLocation = { name: locationName, type: locationType };
    document.getElementById('rating').value = '';
    modal.querySelectorAll('.star-rating span').forEach(star => star.innerHTML = '☆');
    modal.style.display = 'block';
}

// Closes the review form modal
function closeReviewForm() {
    const modal = document.getElementById('reviewFormModal');
    if (modal) modal.style.display = 'none';
}
