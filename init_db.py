import sqlite3
import json

# Load the JSON data
with open("example_orders.json", "r") as f:
    orders_data = json.load(f)

# Connect to the SQLite database
conn = sqlite3.connect("db.sqlite")
cursor = conn.cursor()

# Drop existing tables if they exist
cursor.execute("DROP TABLE IF EXISTS orders;")
cursor.execute("DROP TABLE IF EXISTS items;")
cursor.execute("DROP TABLE IF EXISTS customers;")

# Create tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT NOT NULL UNIQUE
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    item_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 1,
    FOREIGN KEY (customer_id) REFERENCES customers (id),
    FOREIGN KEY (item_id) REFERENCES items (id)
);
""")

# Insert data into tables
customer_cache = {}
item_cache = {}

for order in orders_data:
    # Insert customer if not already added
    customer_key = (order["name"], order["phone"])
    if customer_key not in customer_cache:
        cursor.execute("""
        INSERT INTO customers (name, phone) VALUES (?, ?)
        """, customer_key)
        customer_cache[customer_key] = cursor.lastrowid

    customer_id = customer_cache[customer_key]

    for item in order["items"]:
        # Insert item if not already added
        item_key = (item["name"], item["price"])
        if item_key not in item_cache:
            cursor.execute("""
            INSERT INTO items (name, price) VALUES (?, ?)
            """, item_key)
            item_cache[item_key] = cursor.lastrowid

        item_id = item_cache[item_key]

        # Insert order
        cursor.execute("""
        INSERT INTO orders (customer_id, item_id, quantity) VALUES (?, ?, ?)
        """, (customer_id, item_id, 1))  # Assuming quantity is always 1 in this JSON

# Commit changes and close the connection
conn.commit()
conn.close()

print("Database initialized with data from example_orders.json!")
