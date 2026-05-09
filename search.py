import sqlite3
from trie import Trie


class RestaurantSearchEngine:
    """Search engine for restaurants using trie structure"""
    
    def __init__(self):
        self.restaurant_trie = Trie()
        self.food_item_trie = Trie()
        self._load_data()
    
    def _load_data(self):
        """Load restaurant names and food items into trie"""
        try:
            # Load restaurants
            con = sqlite3.connect('instance/booleanData.db')
            cur = con.cursor()
            cur.execute("SELECT restaurantName FROM booleanData")
            restaurants = cur.fetchall()
            con.close()
            
            for restaurant in restaurants:
                name = restaurant[0]
                self.restaurant_trie.insert(name, {'name': name})
            
            print(f"Loaded {len(restaurants)} restaurants into trie")
        
        except Exception as e:
            print(f"Error loading restaurant data: {e}")
    
    def search_restaurants(self, query, limit=10):
        """
        Search for restaurants by prefix
        
        Args:
            query: Search term
            limit: Max number of results
            
        Returns: List of restaurant names matching query
        """
        results = self.restaurant_trie.autocomplete(query, limit)
        return [result[0].title() for result in results]
    
    def get_restaurant_details(self, name):
        """Get full details for a restaurant"""
        try:
            varData = sqlite3.connect('instance/quantifiableData.db')
            cur = varData.cursor()
            cur.execute("SELECT restaurantName, avgPrice, rating FROM quantifiable WHERE restaurantName = ?", (name,))
            result = cur.fetchone()
            varData.close()
            
            if result:
                return {
                    'name': result[0],
                    'price': result[1],
                    'rating': result[2]
                }
            return None
        except Exception as e:
            print(f"Error getting restaurant details: {e}")
            return None


# Global search engine instance
search_engine = RestaurantSearchEngine()
