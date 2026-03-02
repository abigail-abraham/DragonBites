import sqlite3

def avgRatings():
    #opens the text file and reads the lines
    ratingsFile = open("DragonBites.txt", "r")
    lnes = ratingsFile.readlines()
    ratingsFile.close()
    #initialize dictionaries for total sum and the count for each restaurant (in order to track each rating per restaurant)
    sum = {}
    count = {}
    #track each line, strip the beginning characters and split based on commas so we can iterate through each 
    # element in the txt file
    for line in lnes:
        stripped = line.strip()
        splitLines = stripped.split(",")
        #strip the double quotes in front of the rating and the restaurant
        restaurant = splitLines[0].strip('"')
        rating = splitLines[1].strip('"')
        #check to see if the rating is a number
        if rating.isdigit():
            rating = int(rating)
        #check if the restaurant is already in the dictionary, if it is not, then add the restaurant as a new key and set its inital value to zero
            if restaurant not in sum:
                sum[restaurant] = rating
                count[restaurant] = 1
        #if the restaurant is already in the dictionary, then add the new rating number to the initial value, and update the count of the restaurant
            else:
                sum[restaurant] += rating
                count[restaurant] += 1
    #this for loop is used to calculate the average of each restaurant, use the sum of all of the ratings and divide it by the amount of times the restaurant showed up in the text file
    #this will inevitably result in the final average of each restaurant's rating
    
    data=[]
    for restaurant in sum:
        avg = round(sum[restaurant]/count[restaurant],1)
        data.append(restaurant)
        data.append(avg)
    return data

data=avgRatings()
def updateDatabase(data):
    #connect to the database and update the rating for each restaurant based on the average ratings calculated from the text file
    con = sqlite3.connect('instance/quantifiableData.db')
    cur = con.cursor()
    for i in range(0, len(data), 2):
        restaurant = data[i]
        avg_rating = data[i+1]
        #update the rating for the restaurant in the database
        cur.execute("UPDATE quantifiable SET rating = ? WHERE restaurantName = ?", (avg_rating, restaurant))
    con.commit()
    con.close()

updateDatabase(data)
