from fastapi import FastAPI, HTTPException, Query
from typing import Optional, List
from pydantic import BaseModel, Field
import sqlite3

# Initialize the FastAPI app
app = FastAPI()

# Pydantic models for data validation
class Customer(BaseModel):
    name: str
    phone: str = Field(..., pattern=r"^\d{3}-\d{3}-\d{4}$")

class Item(BaseModel):
    name: str
    price: float

class Order(BaseModel):
    customer_id: int
    item_id: int
    quantity: int

# Database helper function
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
        cursor.execute("INSERT INTO customers (name, phone) VALUES (?, ?)", (customer.name, customer.phone))
        conn.commit()
        customer_id = cursor.lastrowid
        return {"id": customer_id, "name": customer.name, "phone": customer.phone}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Customer with this phone already exists.")
    finally:
        conn.close()

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


 # Added Filtered Feature
    
@app.get("/customers")
def list_customers(
    limit: int = Query(10, ge=1, le=100, description="Number of customers to retrieve (1-100)"),
    name: Optional[str] = Query(None, description="Filter by customer name"),
    phone: Optional[str] = Query(None, description="Filter by customer phone")
):
    conn = connect_db()
    cursor = conn.cursor()

    # Build the query dynamically based on provided filters
    query = "SELECT * FROM customers"
    filters = []
    params = []

    if name:
        filters.append("name LIKE ?")
        params.append(f"%{name}%")

    if phone:
        filters.append("phone = ?")
        params.append(phone)

    if filters:
        query += " WHERE " + " AND ".join(filters)

    query += " LIMIT ?"
    params.append(limit)
    cursor.execute(query, tuple(params))
    rows = cursor.fetchall()
    conn.close()

    if rows:
        return [dict(zip([column[0] for column in cursor.description], row)) for row in rows]
    else:
        return []

@app.delete("/customers/{id}")
def delete_customer(id: int):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM customers WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return {"message": "Customer deleted successfully"}

@app.put("/customers/{id}")
def update_customer(id: int, customer: Customer):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE customers SET name = ?, phone = ? WHERE id = ?", (customer.name, customer.phone, id))
    conn.commit()
    conn.close()
    return {"message": "Customer updated successfully"}

# Items Endpoints
@app.post("/items")
def create_item(item: Item):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO items (name, price) VALUES (?, ?)", (item.name, item.price))
    conn.commit()
    item_id = cursor.lastrowid
    conn.close()
    return {"id": item_id, "name": item.name, "price": item.price}

@app.get("/items/{id}")
def get_item(id: int):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items WHERE id = ?", (id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    else:
        raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/items/{id}")
def delete_item(id: int):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM items WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return {"message": "Item deleted successfully"}

@app.put("/items/{id}")
def update_item(id: int, item: Item):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE items SET name = ?, price = ? WHERE id = ?", (item.name, item.price, id))
    conn.commit()
    conn.close()
    return {"message": "Item updated successfully"}

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
    return {"id": order_id, "customer_id": order.customer_id, "item_id": order.item_id, "quantity": order.quantity}

@app.get("/orders/{id}")
def get_order(id: int):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders WHERE id = ?", (id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    else:
        raise HTTPException(status_code=404, detail="Order not found")

@app.delete("/orders/{id}")
def delete_order(id: int):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM orders WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return {"message": "Order deleted successfully"}

@app.put("/orders/{id}")
def update_order(id: int, order: Order):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE orders SET customer_id = ?, item_id = ?, quantity = ? WHERE id = ?", 
                   (order.customer_id, order.item_id, order.quantity, id))
    conn.commit()
    conn.close()
    return {"message": "Order updated successfully"}
