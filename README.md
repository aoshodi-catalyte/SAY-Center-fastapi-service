# Say-Center-fastapi-service

## Project Description

This project is a FastAPI web service developed collaboratively by the team using GitHub and Cursor. It exposes a product inventory API backed by PostgreSQL for creating, listing, searching, and fetching products by ID.

Products are persisted in the database via SQLAlchemy. The API uses Pydantic `APIProduct` schemas for request/response bodies so clients only see intentional, stable fields — not internal ORM details.

## Prerequisites

- Python 3.11+
- Git
- Cursor (or another code editor)
- [PostgreSQL](https://www.postgresql.org/download/) (local instance)
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

## Database Setup

1. Start PostgreSQL on your machine.
2. Create a database (the default connection expects `say-center`):

   ```sql
   CREATE DATABASE "say-center";
   ```

3. Update the connection string in `src/database.py` if your username, password, host, port, or database name differ from the default:

   ```
   postgresql://postgres:root@localhost:5432/say-center
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
| `POST` | `/products` | Create a new product (returns `201 Created`) |
| `GET` | `/products` | List all products |
| `GET` | `/products/{id}` | Fetch a single product by ID |
| `GET` | `/products/search` | Search products by name (optional `unit` filter) |
| `GET` | `/db-check` | Verify database connectivity and return product count |

### Product fields

When creating a product (`POST /products`), send a JSON body with these fields:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | yes | Product name |
| `unit` | string | yes | Unit of measure (e.g. `"kg"`, `"each"`) |
| `cost_per_unit` | number | yes | Cost per unit (must be ≥ 0) |
| `price_per_unit` | number | yes | Selling price per unit (must be ≥ 0) |
| `quantity_in_stock` | number | yes | Current stock quantity (must be ≥ 0) |

Responses include an auto-generated `id` field. Do not send `id` when creating a product.

### Example responses

**POST /products — 201 Created**

```json
{
  "id": 1,
  "name": "Basil Plant",
  "unit": "each",
  "cost_per_unit": 1.70,
  "price_per_unit": 4.99,
  "quantity_in_stock": 50
}
```

**GET /products — 200 OK**

```json
[
  {
    "id": 1,
    "name": "Basil Plant",
    "unit": "each",
    "cost_per_unit": 1.70,
    "price_per_unit": 4.99,
    "quantity_in_stock": 50
  }
]
```

**GET /products/{id} — 200 OK**

```json
{
  "id": 1,
  "name": "Basil Plant",
  "unit": "each",
  "cost_per_unit": 1.70,
  "price_per_unit": 4.99,
  "quantity_in_stock": 50
}
```

**GET /products/{id} — 400 Bad Request** (product not found)

```json
{
  "detail": "Product does not exist."
}
```

### Search query parameters

`GET /products/search` accepts:

| Parameter | Required | Description |
|-----------|----------|-------------|
| `name` | yes | Exact product name to match |
| `unit` | no | If provided, only return products with this unit |

## How to Try the Endpoints

Use [Postman](https://www.postman.com/downloads/) to send requests to the API. Start PostgreSQL, then start the server:

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

#### 2. Database check — `GET /db-check`

| Setting | Value |
|---------|-------|
| Method | `GET` |
| URL | `http://127.0.0.1:8000/db-check` |

Click **Send**. A successful response looks like:

```json
{"status": "connected", "product_count": 0}
```

#### 3. Create a product — `POST /products`

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
  "id": 1,
  "name": "Basil Plant",
  "unit": "each",
  "cost_per_unit": 1.70,
  "price_per_unit": 4.99,
  "quantity_in_stock": 50
}
```

#### 4. List all products — `GET /products`

| Setting | Value |
|---------|-------|
| Method | `GET` |
| URL | `http://127.0.0.1:8000/products` |

Click **Send**. You will see an array of all products stored in the database.

#### 5. Get a product by ID — `GET /products/{id}`

| Setting | Value |
|---------|-------|
| Method | `GET` |
| URL | `http://127.0.0.1:8000/products/1` |

Replace `1` with the product ID returned from **POST /products**. Click **Send** to retrieve that product.

#### 6. Search products — `GET /products/search`

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

1. Start PostgreSQL and confirm your connection settings in `src/database.py`.
2. Start the server with `uvicorn product_service:app --reload --app-dir src`.
3. Open Postman and import the API from `http://127.0.0.1:8000/openapi.json`, or create the requests manually.
4. Send **GET /db-check** to confirm the database is reachable.
5. Send **POST /products** to add one or more products.
6. Send **GET /products** to confirm they were saved.
7. Send **GET /products/{id}** using the `id` from the create response.
8. Send **GET /products/search** with a `name` query param to find a product.

---

## Database Support

### PostgreSQL Dependencies

PostgreSQL support is provided by `psycopg2-binary`, which is already listed in `requirements.txt` and installed with:

```bash
pip install -r requirements.txt
```

### Database Connection Configuration

Database connection details are configured in `src/database.py` using SQLAlchemy. Update the `DATABASE_URL` value to match your local Postgres setup:

```
postgresql://username:password@localhost:5432/your_database
```

### Models

- **`APIProduct`** (`src/product/models.py`) — Pydantic schema used for API request/response validation.
- **`SQLProduct`** (`src/product/models.py`) — SQLAlchemy model mapped to the `products` table for persistence.

Route handlers in `src/product_service.py` convert between these layers: incoming requests are validated as `APIProduct`, saved as `SQLProduct`, and returned to clients as `APIProduct`.

### Schema Management

> **Warning:**  
> **On every application startup (development mode), the database schema is _dropped and recreated_ automatically. This means all data will be deleted each time you restart the FastAPI app.**  
> _Don't use this mode in production._

This is handled in `src/product_service.py` with:

```python
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
```

- **`drop_all()`** removes all existing tables.
- **`create_all()`** recreates them for your current models.

This keeps your schema in sync during development and helps quickly iterate on model changes. Once schema management is updated for production, products will persist across server restarts as intended.
