import sqlite3
def extractInformation():
        file = open("information.txt","r")
        p=[]
        for line in file:
                if "\n" in line: line=line.replace("\n","")
                p.append(line)
        for i in range(len(p)):
                p[i]=tuple(p[i].split(","))
        file.close()
        return p

def booleanInsertion(n):
        con = sqlite3.connect('booleanData.db')
        cur = con.cursor()
        cur.execute("INSERT INTO booleanData (restaurantName,dragonDollars,diningDollars,takesCard,takesCash) Values "+ str(n))
        con.commit()
        con.close()
info=extractInformation()

def insertNewInformation(info):
        for i in range(len(info)):
                booleanInsertion(info[i])

insertNewInformation(info)
         

