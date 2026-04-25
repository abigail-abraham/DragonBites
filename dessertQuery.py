import sqlite3

#executes filters based on user input
class dessertQuery:

    #initializes the class
    def __init__(self):
        self.clauses=[] #stores all of the filters within the class
        self.minPrice=None #minimum price filter
        self.maxPrice=None #maximum price filter

    #When run, it adds the filters to clauses
    def usesDragonDollars(self):
        self.clauses.append("dragonDollars = 1")
    def usesDiningDollars(self):
        self.clauses.append("diningDollars = 1")
    def takesCash(self):
        self.clauses.append("cash = 1")
    def takesCard(self):
        self.clauses.append("card = 1")

    #Price range filters
    def setMinPrice(self, minPrice):
        self.minPrice = minPrice
    def setMaxPrice(self, maxPrice):
        self.maxPrice = maxPrice
    def removeMinPrice(self):
        self.minPrice = None
    def removeMaxPrice(self):
        self.maxPrice = None

    #Removes filters from clauses
    def usesDragonDollarsREMOVE(self):
        self.clauses.remove("dragonDollars = 1")
    def usesDiningDollarsREMOVE(self):
        self.clauses.remove("diningDollars = 1")
    def takesCashREMOVE(self):
        self.clauses.remove("cash = 1")
    def takesCardREMOVE(self):
        self.clauses.remove("card = 1")
    
    #Executes and returns what places fit the criterias
    def executeQueries(self):
        phrase="" #string phrase after the WHERE clause
        con = sqlite3.connect('instance/dessertsB.db')
        cur = con.cursor()

        if len(self.clauses) == 0:
            cur.execute("SELECT restaurantName FROM dessertsB")
            fits=cur.fetchall()
            con.close()
            varData = sqlite3.connect('instance/desserts.db')
            sor = varData.cursor()
            sor.execute("SELECT DessertPlaceName, AvgPrice, Rating FROM dessertsQ")
            table = sor.fetchall()
            varData.close()
            data = []
            for res in table:
                for fit in fits:
                    if res[0] == fit[0]:
                        #Apply price range filter
                        price = res[1]
                        if (self.minPrice is None or price >= self.minPrice) and \
                           (self.maxPrice is None or price <= self.maxPrice):
                            data.append([fit[0] + " " + str(res[1]) + " " + str(res[2])])
            return data
        elif len(self.clauses) == 1:
            phrase= self.clauses[0]
        else:
            phrase =" AND ".join(self.clauses)

        cur.execute("SELECT restaurantName FROM dessertsB WHERE "+phrase)
        fits=cur.fetchall()
        con.close()
        varData = sqlite3.connect('instance/desserts.db')
        sor = varData.cursor()
        sor.execute("SELECT DessertPlaceName, AvgPrice, Rating FROM dessertsQ")
        table = sor.fetchall()
        varData.close()
        data = []        
        for res in table:
            for fit in fits:
                if res[0] == fit[0]:
                    #Apply price range filter
                    price = res[1]
                    if (self.minPrice is None or price >= self.minPrice) and \
                       (self.maxPrice is None or price <= self.maxPrice):
                        data.append([fit[0] + " " + str(res[1]) + " " + str(res[2])])
        return data


#Sample testing code
""""
d = dessertQuery()
d.setMinPrice(20)
d.setMaxPrice(26)
print(d.executeQueries())
"""