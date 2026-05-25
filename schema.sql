-- Schema for food truck data in the Dragon Bites app
CREATE TABLE IF NOT EXISTS food_trucks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    rating TEXT,
    description TEXT,
    website TEXT,
    image_path TEXT
);
