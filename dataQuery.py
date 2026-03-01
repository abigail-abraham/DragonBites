import sqlite3

#executes filters based on user input
class booleanQuery:

    #initializes the class
    def __init__(self):
        self.clauses=[] #stores all of the filters within the class

    #When run, it adds the filters to clauses
    def usesDragonDollars(self):
        self.clauses.append("dragonDollars = 1")
    def usesDiningDollars(self):
        self.clauses.append("diningDollars = 1")
    def takesCash(self):
        self.clauses.append("takesCash = 1")
    def takesCard(self):
        self.clauses.append("takesCard = 1")
    
    #Removes filters from clauses
    def usesDragonDollarsREMOVE(self):
        self.clauses.remove("dragonDollars = 1")
    def usesDiningDollarsREMOVE(self):
        self.clauses.remove("diningDollars = 1")
    def takesCashREMOVE(self):
        self.clauses.remove("takesCash = 1")
    def takesCardREMOVE(self):
        self.clauses.remove("takesCard = 1")
    
    #Executes and returns what places fit the criterias
    def executeQueries(self):
        phrase="" #string phrase after the WHERE clause
        con = sqlite3.connect('instance/booleanData.db')
        cur = con.cursor()

        if len(self.clauses) == 0:
            cur.execute("SELECT restaurantName FROM booleanData")
            fits=cur.fetchall()
            con.close()
            varData = sqlite3.connect('instance/quantifiableData.db')
            sor = varData.cursor()
            sor.execute("SELECT restaurantName, avgPrice, rating FROM quantifiable")
            table = sor.fetchall()
            varData.close()
            data = []
            for res in table:
                for fit in fits:
                    if res[0] == fit[0]:
                        data.append([fit[0] + " " + str(res[1]) + " " + str(res[2])])
            return data
        elif len(self.clauses) == 1:
            phrase= self.clauses[0]
        else:
            phrase =" AND ".join(self.clauses)

        cur.execute("SELECT restaurantName FROM booleanData WHERE "+phrase)
        fits=cur.fetchall()
        con.close()
        varData = sqlite3.connect('instance/quantifiableData.db')
        sor = varData.cursor()
        sor.execute("SELECT restaurantName, avgPrice, rating FROM quantifiable")
        table = sor.fetchall()
        varData.close()
        data = []
        for res in table:
            for fit in fits:
                if res[0] == fit[0]:
                    data.append([fit[0] + " " + str(res[1]) + " " + str(res[2])])
        return data

#Sample testing code
"""
d = booleanQuery()
print(d.executeQueries())
d.usesDragonDollars()
d.takesCash()
print(d.executeQueries())
d.takesCashREMOVE()
print(d.executeQueries())
"""




