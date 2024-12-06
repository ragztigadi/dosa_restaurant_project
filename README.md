### **README.md**

````markdown
# Dosa Restaurant API

This project is a REST API backend for managing a dosa restaurant, built using **FastAPI** and **SQLite**. The API provides CRUD (Create, Read, Update, Delete) operations for customers, items, and orders.

---

## Features

### Supported Endpoints

#### Customers

| Method | Path              | Description                                  |
| ------ | ----------------- | -------------------------------------------- |
| POST   | `/customers`      | Create a customer with a JSON payload.       |
| GET    | `/customers/{id}` | Retrieve a customer by ID.                   |
| DELETE | `/customers/{id}` | Delete a customer by ID.                     |
| PUT    | `/customers/{id}` | Update a customer by ID with a JSON payload. |

#### Items

| Method | Path          | Description                               |
| ------ | ------------- | ----------------------------------------- |
| POST   | `/items`      | Create an item with a JSON payload.       |
| GET    | `/items/{id}` | Retrieve an item by ID.                   |
| DELETE | `/items/{id}` | Delete an item by ID.                     |
| PUT    | `/items/{id}` | Update an item by ID with a JSON payload. |

#### Orders

| Method | Path           | Description                                |
| ------ | -------------- | ------------------------------------------ |
| POST   | `/orders`      | Create an order with a JSON payload.       |
| GET    | `/orders/{id}` | Retrieve an order by ID.                   |
| DELETE | `/orders/{id}` | Delete an order by ID.                     |
| PUT    | `/orders/{id}` | Update an order by ID with a JSON payload. |

---

## Requirements

- Python 3.8 or higher
- SQLite (built into Python)
- FastAPI
- Uvicorn

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/ragztigadi/dosa_restaurant_project.git
cd dosa_restaurant_project
```
````

### 2. Set Up a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate    # For macOS/Linux
.\venv\Scripts\activate     # For Windows
```

### 3. Install Dependencies

```bash
pip install fastapi uvicorn
```

### 4. Initialize the Database

Run the `init_db.py` script to create the database (`db.sqlite`) and populate it with example data.

```bash
python init_db.py
```

---

## Usage

### Start the FastAPI Server

Run the following command to start the server:

```bash
uvicorn main:app --reload
```

The server will run at: [http://127.0.0.1:8000](http://127.0.0.1:8000).

---

## API Examples

### 1. Customers

#### Create a Customer

**POST** `/customers`

```json
{
  "name": "John Doe",
  "phone": "123-456-7890"
}
```

#### Retrieve a Customer

**GET** `/customers/1`

#### Update a Customer

**PUT** `/customers/1`

```json
{
  "name": "Jane Doe",
  "phone": "987-654-3210"
}
```

#### Delete a Customer

**DELETE** `/customers/1`

---

### 2. Items

#### Create an Item

**POST** `/items`

```json
{
  "name": "Masala Dosa",
  "price": 5.99
}
```

#### Retrieve an Item

**GET** `/items/1`

#### Update an Item

**PUT** `/items/1`

```json
{
  "name": "Plain Dosa",
  "price": 4.99
}
```

#### Delete an Item

**DELETE** `/items/1`

---

### 3. Orders

#### Create an Order

**POST** `/orders`

```json
{
  "customer_id": 1,
  "item_id": 1,
  "quantity": 2
}
```

#### Retrieve an Order

**GET** `/orders/1`

#### Update an Order

**PUT** `/orders/1`

```json
{
  "customer_id": 1,
  "item_id": 2,
  "quantity": 3
}
```

#### Delete an Order

**DELETE** `/orders/1`

---

## Testing the API

1. Use the interactive **Swagger UI** at: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).
2. Use **Postman** or `curl` commands to test the endpoints.

### Example `curl` Command

```bash
curl -X POST "http://127.0.0.1:8000/customers" \
-H "Content-Type: application/json" \
-d '{"name": "John Doe", "phone": "123-456-7890"}'
```

---

## Project Structure

```
dosa_restaurant_project/
│
├── main.py             # FastAPI app with endpoints
├── init_db.py          # Script to initialize and populate the SQLite database
├── db.sqlite           # SQLite database file
├── example_orders.json # Example data for initializing the database
├── README.md           # Project documentation
└── venv/               # Virtual environment directory (optional)
```
