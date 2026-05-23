import sqlite3

# Query class for filtering food trucks
class foodTruckQuery:
    
    def __init__(self):
        self.payment_filters = []  # List of payment methods to filter by
        self.dietary_filters = []  # List of dietary options to filter by
        self.min_price = None
        self.max_price = None
    
    # Payment method filters
    def accepts_cash(self):
        if "cash = 1" not in self.payment_filters:
            self.payment_filters.append("cash = 1")
    
    def accepts_card(self):
        if "card = 1" not in self.payment_filters:
            self.payment_filters.append("card = 1")
    
    def accepts_mobile_payment(self):
        if "mobilePaymentService = 1" not in self.payment_filters:
            self.payment_filters.append("mobilePaymentService = 1")
    
    # Dietary option filters
    def is_halal(self):
        if "halal = 1" not in self.dietary_filters:
            self.dietary_filters.append("halal = 1")
    
    def is_vegetarian(self):
        if "vegetarian = 1" not in self.dietary_filters:
            self.dietary_filters.append("vegetarian = 1")
    
    # Price range filters
    def set_min_price(self, min_price):
        self.min_price = min_price
    
    def set_max_price(self, max_price):
        self.max_price = max_price
    
    def execute_query(self):
        """Execute the query and return matching food trucks"""
        con_payment = sqlite3.connect('instance/foodTrucksB.db')
        cur_payment = con_payment.cursor()
        
        # Build payment filter query
        if len(self.payment_filters) > 0:
            payment_where = " OR ".join(self.payment_filters)
            cur_payment.execute(f"SELECT [foodTruck name] FROM [foodTruck payment] WHERE {payment_where}")
        else:
            cur_payment.execute("SELECT [foodTruck name] FROM [foodTruck payment]")
        
        payment_results = set([row[0] for row in cur_payment.fetchall()])
        con_payment.close()
        
        # Get food truck data
        con_data = sqlite3.connect('instance/foodTrucks.db')
        cur_data = con_data.cursor()
        
        # Build dietary filter query
        if len(self.dietary_filters) > 0:
            dietary_where = " AND ".join(self.dietary_filters)
            cur_data.execute(f"SELECT [foodTruck Name], avgPrice, rating FROM foodTrucks WHERE {dietary_where}")
        else:
            cur_data.execute("SELECT [foodTruck Name], avgPrice, rating FROM foodTrucks")
        
        all_trucks = cur_data.fetchall()
        con_data.close()
        
        # Apply filters
        results = []
        for truck_name, avg_price, rating in all_trucks:
            # Check payment method filter
            if len(self.payment_filters) > 0 and truck_name not in payment_results:
                continue
            
            # Check price range filter
            if self.min_price is not None and avg_price < self.min_price:
                continue
            if self.max_price is not None and avg_price > self.max_price:
                continue
            
            results.append({
                'name': truck_name,
                'price': avg_price,
                'rating': rating
            })
        
        return results
