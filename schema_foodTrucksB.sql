-- Schema for foodTrucksB.db payment table in the Dragon Bites app
CREATE TABLE IF NOT EXISTS [foodTruck payment] (
    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
    [foodTruck name] TEXT,
    cash INTEGER NOT NULL,
    card INTEGER NOT NULL,
    mobilePaymentService INTEGER NOT NULL
);
