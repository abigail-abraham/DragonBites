from flask import Flask, jsonify, request, render_template, session
import dataQuery
import dessertQuery
import os

app = Flask(__name__)

# Use an environment-provided SECRET_KEY in production; fall back to a random key for local dev
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

@app.route("/desserts")
def desserts():
    return render_template("desserts.html")

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


# Runs the website
if __name__ == "__main__":
    app.run(debug=True)