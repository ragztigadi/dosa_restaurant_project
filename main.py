from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

# Initialize the FastAPI app
app = FastAPI()

# Pydantic model for validating customer data
class Customer(BaseModel):
    name: str
    phone: str

# Helper function to connect to the SQLite database
def connect_db():
    conn = sqlite3.connect("db.sqlite")
    conn.row_factory = sqlite3.Row  # Return rows as dictionaries
    return conn

# POST endpoint to create a new customer
@app.post("/customers")
def create_customer(customer: Customer):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        # Insert customer into the database
        cursor.execute(
            "INSERT INTO customers (name, phone) VALUES (?, ?)",
            (customer.name, customer.phone),
        )
        conn.commit()
        customer_id = cursor.lastrowid  # Get the auto-generated ID
        return {"id": customer_id, "name": customer.name, "phone": customer.phone}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Customer with this phone already exists.")
    finally:
        conn.close()

# GET endpoint to retrieve a customer by ID
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

# PUT endpoint to update a customer by ID
@app.put("/customers/{id}")
def update_customer(id: int, customer: Customer):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE customers SET name = ?, phone = ? WHERE id = ?",
        (customer.name, customer.phone, id),
    )
    conn.commit()
    conn.close()
    return {"message": "Customer updated successfully"}

# DELETE endpoint to delete a customer by ID
@app.delete("/customers/{id}")
def delete_customer(id: int):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM customers WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return {"message": "Customer deleted successfully"}

# Root endpoint for testing the server
@app.get("/")
def root():
    return {"message": "Welcome to the Dosa Restaurant API!"}
