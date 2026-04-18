import sqlite3
import os

# Create/connect to database
db_path = os.path.join(os.path.dirname(__file__), '..', 'locations.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS locations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        longitude REAL NOT NULL,
        latitude REAL NOT NULL,
        icon TEXT NOT NULL
    )
''')

# Location data extracted from map.js (line 163+)
# Format: [name, longitude, latitude, icon]
locations = [
    ("Tataki Sushi and Ramen", -75.19207226199879, 39.957586599999054, "blueIcon"),
    ("Han Dynasty", -75.19710636677178, 39.95672897997564, "blueIcon"),
    ("Chik-fil-A", -75.19066655281112, 39.95892892006141, "blueIcon"),
    ("Wild Blue Sushi", -75.19051829394947, 39.95892579555406, "blueIcon"),
    ("Chipotle", -75.19139423385867, 39.957211125669666, "blueIcon"),
    ("Sabrina's", -75.19071384179624, 39.959963231800494, "blueIcon"),
    ("Mango Mango", -75.194584, 39.959262, "yellowIcon"),
    ("Carvel", -75.191870, 39.957404, "yellowIcon"),
    ("Kiwi Yogurt", -75.195189, 39.954571, "yellowIcon"),
    ("Surreal Creamery", -75.1800, 39.9529, "yellowIcon"),
    ("Coco's Creamery", -75.195166, 39.959559, "yellowIcon"),
    ("Maison Sweet", -75.183309, 39.953219, "yellowIcon"),
    ("Insomnia Cookies", -75.191708, 39.957366, "yellowIcon"),
]

# Insert data
cursor.executemany(
    'INSERT INTO locations (name, longitude, latitude, icon) VALUES (?, ?, ?, ?)',
    locations
)

conn.commit()
print(f"Successfully inserted {len(locations)} locations into {db_path}")

# Verify the data
cursor.execute('SELECT * FROM locations')
rows = cursor.fetchall()
print(f"\nVerification - Total rows in database: {len(rows)}")
for row in rows:
    print(f"  ID: {row[0]}, Name: {row[1]}, Longitude: {row[2]}, Latitude: {row[3]}, Icon: {row[4]}")

conn.close()
