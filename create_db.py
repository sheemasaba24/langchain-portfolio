import sqlite3

conn = sqlite3.connect("company.db")
cursor = conn.cursor()

# Create tables
cursor.executescript("""
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY,
    name TEXT,
    department TEXT,
    salary REAL,
    join_date TEXT,
    city TEXT
);

CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY,
    name TEXT,
    category TEXT,
    price REAL,
    stock INTEGER
);

CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY,
    employee_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    sale_date TEXT,
    total_amount REAL
);
""")

# Insert employees
cursor.executemany("INSERT OR IGNORE INTO employees VALUES (?,?,?,?,?,?)", [
    (1, "Sheema Saba",   "AI Engineering", 95000, "2023-01-15", "Chennai"),
    (2, "Rahul Sharma",  "Data Science",   88000, "2022-06-01", "Mumbai"),
    (3, "Priya Menon",   "Engineering",    75000, "2023-03-10", "Bangalore"),
    (4, "Arjun Nair",    "Marketing",      65000, "2021-09-20", "Delhi"),
    (5, "Divya Patel",   "Data Science",   92000, "2022-11-05", "Hyderabad"),
    (6, "Karan Singh",   "Engineering",    78000, "2023-07-15", "Pune"),
    (7, "Meena Iyer",    "AI Engineering", 98000, "2021-04-01", "Chennai"),
    (8, "Vikram Das",    "Marketing",      61000, "2022-08-30", "Mumbai"),
])

# Insert products
cursor.executemany("INSERT OR IGNORE INTO products VALUES (?,?,?,?,?)", [
    (1, "AI Analytics Suite",   "Software",  2999, 50),
    (2, "Data Dashboard Pro",   "Software",  1499, 100),
    (3, "ML Model Toolkit",     "Software",  3999, 30),
    (4, "IoT Sensor Pack",      "Hardware",  799,  200),
    (5, "Cloud Storage 1TB",    "Service",   299,  999),
    (6, "Cybersecurity Bundle", "Software",  1999, 75),
])

# Insert sales
cursor.executemany("INSERT OR IGNORE INTO sales VALUES (?,?,?,?,?,?)", [
    (1,  1, 1, 2, "2024-01-10", 5998),
    (2,  2, 3, 1, "2024-01-15", 3999),
    (3,  3, 2, 3, "2024-02-01", 4497),
    (4,  1, 4, 5, "2024-02-10", 3995),
    (5,  5, 1, 1, "2024-02-20", 2999),
    (6,  2, 6, 2, "2024-03-05", 3998),
    (7,  7, 3, 2, "2024-03-10", 7998),
    (8,  4, 5, 4, "2024-03-15", 1196),
    (9,  6, 2, 2, "2024-04-01", 2998),
    (10, 8, 4, 3, "2024-04-10", 2397),
    (11, 1, 3, 1, "2024-04-15", 3999),
    (12, 5, 6, 1, "2024-05-01", 1999),
])

conn.commit()
conn.close()
print("✅ Database created successfully with employees, products and sales!")