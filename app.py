from flask import Flask, jsonify, request, render_template, session
import dataQuery
import dessertQuery
import foodTruckQuery
import search
import os

app = Flask(__name__)

app.secret_key = os.environ.get('SECRET_KEY') or os.urandom(24)

@app.route("/", methods=["GET", "POST"])
def index():
    # Initialize session filters if not exists
    if 'filters' not in session:
        session['filters'] = []
    if 'price_range' not in session:
        session['price_range'] = None
    
    # Handle AJAX JSON requests for filter updates
    if request.is_json:
        data = request.get_json()
        filters = data.get('filters', [])
        min_price = data.get('minPrice')
        max_price = data.get('maxPrice')
        
        session['filters'] = filters
        
        # Store price range in session if provided
        if min_price and max_price:
            try:
                session['price_range'] = (float(min_price), float(max_price))
            except (ValueError, TypeError):
                session['price_range'] = None
        else:
            session['price_range'] = None
        session.modified = True
        
        # Create query with all active filters
        
        b = dataQuery.booleanQuery()
        
        if 'dragonDollars' in session['filters']:
            b.usesDragonDollars()
        if 'diningDollars' in session['filters']:
            b.usesDiningDollars()
        if 'card' in session['filters']:
            b.takesCard()
        if 'cash' in session['filters']:
            b.takesCash()
        
        # Apply price range filter if stored in session
        if session['price_range']:
            min_p, max_p = session['price_range']
            b.pricerange(min_p, max_p)
        
        restaurants = b.executeQueries()
        return jsonify({'restaurants': restaurants})
    
    # Handle regular page load
    # Create query with all active filters
    b = dataQuery.booleanQuery()
    
    if 'dragonDollars' in session['filters']:
        b.usesDragonDollars()
    if 'diningDollars' in session['filters']:
        b.usesDiningDollars()
    if 'card' in session['filters']:
        b.takesCard()
    if 'cash' in session['filters']:
        b.takesCash()
    
    # Apply price range filter if stored in session
    if session['price_range']:
        min_p, max_p = session['price_range']
        b.pricerange(min_p, max_p)
    
    restaurants = b.executeQueries()
    
    return render_template("website.html", restaurants=restaurants, active_filters=session['filters'])

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/listing")
def listing():
    return render_template("restaurant_Abigail.html")

@app.route("/api/filter-restaurants", methods=["POST"])
def filter_restaurants():
    data = request.get_json()
    
    # Create restaurant query object
    rq = dataQuery.booleanQuery()
    
    # Apply payment method filters
    filters = data.get('filters', [])
    if 'dragonDollars' in filters:
        rq.usesDragonDollars()
    if 'diningDollars' in filters:
        rq.usesDiningDollars()
    if 'card' in filters:
        rq.takesCard()
    if 'cash' in filters:
        rq.takesCash()
    
    # Apply price range filters
    min_price = data.get('minPrice')
    max_price = data.get('maxPrice')
    
    if min_price is not None:
        try:
            rq.setMinPrice(float(min_price))
        except (ValueError, TypeError):
            pass
    
    if max_price is not None:
        try:
            rq.setMaxPrice(float(max_price))
        except (ValueError, TypeError):
            pass
    
    # Execute query and return results
    results = rq.executeQueries()
    return jsonify({'restaurants': results})

@app.route("/desserts")
def desserts():
    return render_template("desserts.html")

@app.route("/food-trucks")
def food_trucks():
    return render_template("food_trucks.html")

@app.route("/api/filter-food-trucks", methods=["POST"])
def filter_food_trucks():
    """API endpoint for filtering food trucks"""
    data = request.get_json()
    
    # Create food truck query object
    ftq = foodTruckQuery.foodTruckQuery()
    
    # Apply payment method filters
    filters = data.get('filters', [])
    if 'cash' in filters:
        ftq.accepts_cash()
    if 'card' in filters:
        ftq.accepts_card()
    if 'mobilePayment' in filters:
        ftq.accepts_mobile_payment()
    
    # Apply dietary filters
    if 'vegetarian' in filters:
        ftq.is_vegetarian()
    if 'halal' in filters:
        ftq.is_halal()
    
    # Apply price range filters
    min_price = data.get('minPrice')
    max_price = data.get('maxPrice')
    
    if min_price is not None:
        try:
            ftq.set_min_price(float(min_price))
        except (ValueError, TypeError):
            pass
    
    if max_price is not None:
        try:
            ftq.set_max_price(float(max_price))
        except (ValueError, TypeError):
            pass
    
    # Execute query and return results
    results = ftq.execute_query()
    return jsonify({'foodTrucks': results})

@app.route("/api/search-restaurants", methods=["GET"])
def search_restaurants():
    """API endpoint for restaurant autocomplete search using trie"""
    query = request.args.get('q', '').strip()
    limit = request.args.get('limit', 10, type=int)
    
    if not query or len(query) < 1:
        return jsonify({'results': []})
    
    results = search.search_engine.search_restaurants(query, limit)
    return jsonify({'results': results})

@app.route("/api/filter-desserts", methods=["POST"])
def filter_desserts():
    data = request.get_json()
    
    # Create dessert query object
    dq = dessertQuery.dessertQuery()
    
    # Apply payment method filters
    filters = data.get('filters', [])
    if 'dragonDollars' in filters:
        dq.usesDragonDollars()
    if 'diningDollars' in filters:
        dq.usesDiningDollars()
    if 'card' in filters:
        dq.takesCard()
    if 'cash' in filters:
        dq.takesCash()
    
    # Apply price range filters
    min_price = data.get('minPrice')
    max_price = data.get('maxPrice')
    
    if min_price is not None:
        try:
            dq.setMinPrice(float(min_price))
        except (ValueError, TypeError):
            pass
    
    if max_price is not None:
        try:
            dq.setMaxPrice(float(max_price))
        except (ValueError, TypeError):
            pass
    
    # Execute query and return results
    results = dq.executeQueries()
    return jsonify({'desserts': results})

@app.route("/meal-mapper")
def mealmapper():
    return render_template("mealmapper.html")

# Write A Review Section - I added this so users can leave ratings and comments on Restaurants, Desserts, and Food Trucks Pages (they can delete their comment too).
# The database is instance/reviews.db

@app.route('/get_reviews', methods=['POST'])
def get_reviews():
    # Gets all reviews for a specific location (restaurant/dessert/food truck)
    # Called by JavaScript when a modal opens
    import sqlite3
    data = request.get_json()
    location_name = data.get('location_name')
    location_type = data.get('location_type')
    
    conn = sqlite3.connect('instance/reviews.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, author_name, rating, comment, date 
        FROM reviews 
        WHERE location_name = ? AND location_type = ?
        ORDER BY date DESC
    ''', (location_name, location_type))
    
    reviews = cursor.fetchall()
    conn.close()
    
    reviews_list = []
    for review in reviews:
        reviews_list.append({
            'id': review[0],
            'author_name': review[1],
            'rating': review[2],
            'comment': review[3],
            'date': review[4]
        })
    
    return jsonify({'reviews': reviews_list})

@app.route('/add_review', methods=['POST'])
def add_review():
    # Saves a new review to the database
    # Gets name, rating, comment from the form
    import sqlite3
    data = request.get_json()
    
    location_name = data.get('location_name')
    location_type = data.get('location_type')
    rating = data.get('rating')
    comment = data.get('comment')
    author_name = data.get('author_name', 'Anonymous')
    
    if not author_name or author_name.strip() == '':
        author_name = 'Anonymous'
    
    conn = sqlite3.connect('instance/reviews.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO reviews (location_name, location_type, rating, comment, author_name)
        VALUES (?, ?, ?, ?, ?)
    ''', (location_name, location_type, rating, comment, author_name))
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'message': 'Review added successfully!'})

@app.route('/delete_review', methods=['POST'])
def delete_review():
    # Deletes a review when user clicks the trash button
    import sqlite3
    data = request.get_json()
    review_id = data.get('review_id')
    
    conn = sqlite3.connect('instance/reviews.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM reviews WHERE id = ?', (review_id,))
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'message': 'Review deleted successfully!'})

# Runs the website
if __name__ == "__main__":
    app.run(debug=True)