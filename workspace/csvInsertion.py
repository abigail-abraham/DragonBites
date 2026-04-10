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
#take the csv data and insert it into the file, format data entry using this      
def booleanInsertion(n):
        con = sqlite3.connect('instance/booleanData.db')
        cur = con.cursor()
        cur.execute("INSERT INTO booleanData (restaurantName,dragonDollars,diningDollars,takesCard,takesCash) Values "+ str(n))
        con.commit()
        con.close()

def quantityInsertion(n):
        con = sqlite3.connect('instance/quantifiableData.db')
        cur = con.cursor()
        cur.execute("INSERT INTO quantifiable (restaurantName,rating,avgPrice) Values "+ str(n))
        con.commit()
        con.close()

def insertNewInformation(info):
        for i in range(len(info)):
                #booleanInsertion(info[i])
                quantityInsertion(info[i])
info= extractInformation()
insertNewInformation(info)
