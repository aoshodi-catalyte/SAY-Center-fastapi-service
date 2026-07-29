# Say-Center-fastapi-service

## Project Description

This project is a FastAPI web service developed collaboratively by the team using GitHub and Cursor. It exposes a product inventory API backed by PostgreSQL for creating, listing, searching, updating, and soft-deleting products by ID.

Products are persisted in the database via SQLAlchemy. Request bodies are validated with the Pydantic `APIProduct` schema; responses use `ProductResponse` so clients only see intentional, stable fields — not internal ORM details.

## Prerequisites

- Python 3.12+
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

## Environment Setup

Create a `.env` file in the project root with your PostgreSQL connection string:

```
DATABASE_URL=postgresql://username:password@host:port/database
```

Adjust username, password, host, port, and database name to match your local setup. The app loads this value via `src/config.py` using `pydantic-settings`.

## Database Setup

1. Start PostgreSQL on your machine.
2. Create a database:

   ```sql
   CREATE DATABASE "say-center";
   ```

3. Set `DATABASE_URL` in your `.env` file if your credentials or database name differ from the default.

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
| `GET` | `/products` | List all active products |
| `GET` | `/products/{id}` | Fetch a single active product by ID |
| `GET` | `/products/search` | Search active products by name (optional `unit` filter) |
| `GET` | `/db-check` | Verify database connectivity and return product count |
| `PUT` | `/products/{id}` | Update an active product with the given ID |
| `DELETE` | `/products/{id}` | Soft-delete a product (sets `active` to `false`; returns `204 No Content`) |

Inactive (soft-deleted) products are excluded from list, get-by-id, and search responses.

### Product fields

When creating or updating a product (`POST /products` or `PUT /products/{id}`), send a JSON body with these fields:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | yes | Product name (cannot be empty or whitespace-only) |
| `unit` | string | yes | Unit of measure — must be one of: `each`, `lb`, `kg`, `bag`, `box` |
| `cost_per_unit` | number | yes | Cost per unit (must be ≥ 0) |
| `price_per_unit` | number | yes | Selling price per unit (must be > 0) |
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

**GET /products/{id} — 404 Not Found** (product not found)

```json
{
  "detail": "Product does not exist."
}
```

**PUT /products/{id} — 200 OK**

```json
{
  "id": 1,
  "name": "Updated Basil Plant",
  "unit": "kg",
  "cost_per_unit": 2.00,
  "price_per_unit": 5.99,
  "quantity_in_stock": 25
}
```

**PUT /products/{id} — 404 Not Found** (product not found)

```json
{
  "detail": "Product does not exist"
}
```

**DELETE /products/{id} — 204 No Content** (empty body)

**DELETE /products/{id} — 404 Not Found** (product not found)

```json
{
  "detail": "Product does not exist"
}
```

### Search query parameters

`GET /products/search` accepts:

| Parameter | Required | Description |
|-----------|----------|-------------|
| `name` | yes | Exact product name to match |
| `unit` | no | If provided, only return products with this unit |

## How to Try the Endpoints

Use [Postman](https://www.postman.com/downloads/) to send requests to the API. Start PostgreSQL, configure your `.env` file, then start the server:

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

Click **Send**. You will see an array of all active products stored in the database.

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

#### 7. Update a product — `PUT /products/{id}`

| Setting | Value |
|---------|-------|
| Method | `PUT` |
| URL | `http://127.0.0.1:8000/products/1` |
| Body | **raw** → **JSON** |

Replace `1` with the product ID. Use the same JSON body shape as **POST /products**. Click **Send**. A successful response returns `200 OK` with the updated product.

#### 8. Delete a product — `DELETE /products/{id}`

| Setting | Value |
|---------|-------|
| Method | `DELETE` |
| URL | `http://127.0.0.1:8000/products/1` |

Replace `1` with the product ID. Click **Send**. A successful response returns `204 No Content` with an empty body. The product is soft-deleted and will no longer appear in list, get, or search results.

### Suggested workflow

1. Start PostgreSQL and set `DATABASE_URL` in your `.env` file.
2. Start the server with `uvicorn product_service:app --reload --app-dir src`.
3. Open Postman and import the API from `http://127.0.0.1:8000/openapi.json`, or create the requests manually.
4. Send **GET /db-check** to confirm the database is reachable.
5. Send **POST /products** to add one or more products.
6. Send **GET /products** to confirm they were saved.
7. Send **GET /products/{id}** using the `id` from the create response.
8. Send **GET /products/search** with a `name` query param to find a product.
9. Send **PUT /products/{id}** to update a product.
10. Send **DELETE /products/{id}** to soft-delete a product.

---

## Database Support

### PostgreSQL Dependencies

PostgreSQL support is provided by `psycopg2-binary`, which is already listed in `requirements.txt` and installed with:

```bash
pip install -r requirements.txt
```

### Database Connection Configuration

Database connection details are loaded from the `DATABASE_URL` environment variable (via `.env` and `src/config.py`) and used in `src/database.py` with SQLAlchemy:

```
postgresql://username:password@localhost:5432/your_database
```

### Models

- **`APIProduct`** (`src/product/APIProduct.py`) — Pydantic schema for validating create and update request bodies.
- **`ProductResponse`** (`src/product/ProductResponse.py`) — Pydantic schema for API responses.
- **`SQLSchema`** (`src/product/SQLSchema.py`) — SQLAlchemy model mapped to the `products` table for persistence.

Route handlers in `src/product_service.py` convert between these layers: incoming requests are validated as `APIProduct`, saved as `SQLSchema`, and returned to clients as `ProductResponse`.

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


## Contributors
<a href="https://github.com/aoshodi-catalyte/SAY-Center-fastapi-service/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=aoshodi-catalyte/SAY-Center-fastapi-service/"/>
</a>
