# Say-Center-fastapi-service

## Project Description

This project is a FastAPI web service developed collaboratively by the team using GitHub and Cursor. It exposes a product inventory API for creating, listing, and searching products.

## Prerequisites

- Python 3.11+
- Git
- Cursor (or another code editor)
- FastAPI
- Uvicorn
- [Postman](https://www.postman.com/downloads/) (for testing endpoints)

## Clone the Repository

```bash
git clone <repository-url>
cd SAY-Center-fastapi-service
```

## Venv Setup

Create and activate a virtual environment:

```bash
python -m venv .venv
```

**PowerShell**

```powershell
.venv\Scripts\Activate.ps1
```

**Bash (Git Bash / WSL / macOS / Linux)**

```bash
source .venv/Scripts/activate   # Windows
source .venv/bin/activate       # macOS / Linux
```

## Install Steps

```bash
pip install -r requirements.txt
```

## How to Run the App

From the project root, start the product service:

```bash
uvicorn product_service:app --reload --app-dir src
```

The API will be available at `http://127.0.0.1:8000`.

> **Note:** `src/main.py` contains an earlier hello-world app. Run it with `uvicorn main:app --reload --app-dir src` if you want to try those endpoints instead.

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/` | Health check — returns a welcome message |
| `POST` | `/products` | Create a new product |
| `GET` | `/products` | List all products |
| `GET` | `/products/search` | Search products by name (optional `unit` filter) |

### Product fields

When creating a product (`POST /products`), send a JSON body with these fields:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | yes | Product name |
| `unit` | string | yes | Unit of measure (e.g. `"kg"`, `"each"`) |
| `cost_per_unit` | number | yes | Cost per unit (must be ≥ 0) |
| `price_per_unit` | number | yes | Selling price per unit (must be ≥ 0) |
| `quantity_in_stock` | number | yes | Current stock quantity (must be ≥ 0) |

### Search query parameters

`GET /products/search` accepts:

| Parameter | Required | Description |
|-----------|----------|-------------|
| `name` | yes | Exact product name to match |
| `unit` | no | If provided, only return products with this unit |

## How to Try the Endpoints

Use [Postman](https://www.postman.com/downloads/) to send requests to the API. Start the server first:

```bash
uvicorn product_service:app --reload --app-dir src
```

The base URL for all requests is `http://127.0.0.1:8000`.

### Import the API into Postman (optional)

With the server running, you can import all endpoints at once:

1. Open Postman and click **Import**.
2. Choose **Link** and paste: `http://127.0.0.1:8000/openapi.json`
3. Click **Continue**, then **Import**.

Postman will create a collection with every endpoint pre-configured. You can skip the manual steps below if you use this option.

### Manual requests in Postman

Create a new collection (e.g. **Say Center Products**) and add the following requests.

#### 1. Health check — `GET /`

| Setting | Value |
|---------|-------|
| Method | `GET` |
| URL | `http://127.0.0.1:8000/` |

Click **Send**. You should receive:

```json
{"message": "Hello!"}
```

#### 2. Create a product — `POST /products`

| Setting | Value |
|---------|-------|
| Method | `POST` |
| URL | `http://127.0.0.1:8000/products` |
| Body | **raw** → **JSON** |

Body example:

```json
{
  "name": "Basil Plant",
  "unit": "each",
  "cost_per_unit": 1.70,
  "price_per_unit": 4.99,
  "quantity_in_stock": 50
}
```

Click **Send**. A successful response looks like:

```json
{
  "message": "New Product added successfully!",
  "product": {
    "name": "Basil Plant",
    "unit": "each",
    "cost_per_unit": 1.70,
    "price_per_unit": 4.99,
    "quantity_in_stock": 50
  }
}
```

#### 3. List all products — `GET /products`

| Setting | Value |
|---------|-------|
| Method | `GET` |
| URL | `http://127.0.0.1:8000/products` |

Click **Send**. You will see an array of all products currently in memory.

#### 4. Search products — `GET /products/search`

| Setting | Value |
|---------|-------|
| Method | `GET` |
| URL | `http://127.0.0.1:8000/products/search` |

Go to the **Params** tab and add:

| Key | Value | Required |
|-----|-------|----------|
| `name` | `Basil Plant` | yes |
| `unit` | `each` | no |

Click **Send**. Matching products are returned as a JSON array.

### Suggested workflow

1. Start the server with `uvicorn product_service:app --reload --app-dir src`.
2. Open Postman and import the API from `http://127.0.0.1:8000/openapi.json`, or create the requests manually.
3. Send **POST /products** to add one or more products.
4. Send **GET /products** to confirm they were saved.
5. Send **GET /products/search** with a `name` query param to find a product.

---

## Database Support

### PostgreSQL Dependencies

To use PostgreSQL as your database backend, make sure you have the required dependencies installed:

```
pip install psycopg2-binary
```

This package is already listed in `requirements.txt` as `psycopg2-binary`.

### Database Connection Configuration

Database connection details are configured in the `database.py` file using SQLAlchemy. 
Typically, your database URL is set as an environment variable, for example:

```
DATABASE_URL=postgresql://username:password@localhost:5432/your_database
```

Make sure to adjust these values according to your own Postgres setup.

### SQLAlchemy Model

The `Product` table is defined as a SQLAlchemy model (see `models.py`). 
This enables fast database access and integration with FastAPI.

### Schema Management

> **Warning:**  
> **On every application startup (development mode), the database schema is _dropped and recreated_ automatically. This means all data will be deleted each time you restart the FastAPI app.**  
> _Don't use this mode in production._

This is handled in `product_service.py` with:

```python
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
```

- **`drop_all()`** removes all existing tables.
- **`create_all()`** recreates them for your current models.

This keeps your schema in sync during development and helps quickly iterate on model changes.

---

**Next Steps:**

- Start PostgreSQL on your machine.
- Set the appropriate `DATABASE_URL` in your environment or `.env` file.
- Start the app with:

  ```
  uvicorn product_service:app --reload --app-dir src
  ```

You can now safely use the FastAPI endpoints above. Remember, all product data will reset on every server restart during development!