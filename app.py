from flask import Flask, jsonify, request, render_template, session
import dataQuery
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
    
    return render_template("website2.html", restaurants=restaurants, active_filters=session['filters'])

if __name__ == "__main__":
    app.run(debug=True)