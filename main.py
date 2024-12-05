from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

# Initialize the FastAPI app
app = FastAPI()

# Pydantic model for validating customer data
class Customer(BaseModel):
    name: str
    phone: str

# Pydantic model for validating item data
class Item(BaseModel):
    name: str
    price: float

# Pydantic model for validating order data
class Order(BaseModel):
    customer_id: int
    item_id: int
    quantity: int

# Helper function to connect to the SQLite database
def connect_db():
    conn = sqlite3.connect("db.sqlite")
    conn.row_factory = sqlite3.Row  # Return rows as dictionaries
    return conn

# Customers Endpoints
@app.post("/customers")
def create_customer(customer: Customer):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO customers (name, phone) VALUES (?, ?)", 
                       (customer.name, customer.phone))
        conn.commit()
        customer_id = cursor.lastrowid
        return {"id": customer_id, "name": customer.name, "phone": customer.phone}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Customer with this phone already exists.")
    finally:
        conn.close()

@app.get("/customers")
def list_customers(name: str = None):
    conn = connect_db()
    cursor = conn.cursor()
    if name:
        cursor.execute("SELECT * FROM customers WHERE name LIKE ?", (f"%{name}%",))
    else:
        cursor.execute("SELECT * FROM customers")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

@app.get("/customers/{id}")
def get_customer(id: int):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customers WHERE id = ?", (id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    else:
        raise HTTPException(status_code=404, detail="Customer not found")

@app.put("/customers/{id}")
def update_customer(id: int, customer: Customer):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE customers SET name = ?, phone = ? WHERE id = ?", 
                   (customer.name, customer.phone, id))
    conn.commit()
    conn.close()
    return {"message": "Customer updated successfully"}

@app.delete("/customers/{id}")
def delete_customer(id: int):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM customers WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return {"message": "Customer deleted successfully"}

# Items Endpoints
@app.post("/items")
def create_item(item: Item):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO items (name, price) VALUES (?, ?)", 
                   (item.name, item.price))
    conn.commit()
    item_id = cursor.lastrowid
    conn.close()
    return {"id": item_id, "name": item.name, "price": item.price}

@app.get("/items")
def list_items(name: str = None):
    conn = connect_db()
    cursor = conn.cursor()
    if name:
        cursor.execute("SELECT * FROM items WHERE name LIKE ?", (f"%{name}%",))
    else:
        cursor.execute("SELECT * FROM items")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

# Orders Endpoints
@app.post("/orders")
def create_order(order: Order):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO orders (customer_id, item_id, quantity) VALUES (?, ?, ?)", 
                   (order.customer_id, order.item_id, order.quantity))
    conn.commit()
    order_id = cursor.lastrowid
    conn.close()
    return {"id": order_id, "customer_id": order.customer_id, 
            "item_id": order.item_id, "quantity": order.quantity}

@app.get("/orders")
def list_orders(customer_id: int = None):
    conn = connect_db()
    cursor = conn.cursor()
    if customer_id:
        cursor.execute("SELECT * FROM orders WHERE customer_id = ?", (customer_id,))
    else:
        cursor.execute("SELECT * FROM orders")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]
