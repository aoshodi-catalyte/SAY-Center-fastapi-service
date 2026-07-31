# Say-Center-fastapi-service

**Version:** 0.1.0

## Project Description

This project is a FastAPI web service developed collaboratively by the team using GitHub and Cursor. It exposes a product inventory API backed by PostgreSQL for managing categories and products — including create, list, search, update, and soft-delete operations.

Products belong to categories via a foreign key. Request bodies are validated with Pydantic schemas (`ProductModel`, `CategoryModel`); responses use read schemas (`ProductRead`, `CategoryRead`, `CategoryReadWithProducts`) so clients only see intentional, stable fields — not internal ORM details.

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

From the project root, start the application:

```bash
uvicorn main:app --reload --app-dir src
```

The API will be available at `http://127.0.0.1:8000`.

The app is defined in `src/main.py` and mounts both the category and product routers.

## API Endpoints

### Categories

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/categories` | Create a new category (returns `201 Created`) |
| `GET` | `/categories` | List all categories |
| `GET` | `/categories/{id}` | Fetch a category by ID, including its products |

### Products

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/products` | Create a new product (returns `201 Created`) |
| `GET` | `/products` | List all active products |
| `GET` | `/products/{id}` | Fetch a single active product by ID |
| `GET` | `/products/search` | Search active products by name (optional `unit` filter) |
| `GET` | `/db-check` | Verify database connectivity and return product count |
| `PUT` | `/products/{id}` | Update an active product with the given ID |
| `DELETE` | `/products/{id}` | Soft-delete a product (sets `active` to `false`; returns `204 No Content`) |

Inactive (soft-deleted) products are excluded from list, get-by-id, and search responses.

### Category fields

When creating a category (`POST /categories`), send a JSON body with:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | yes | Category name (cannot be empty or whitespace-only) |

Responses include an auto-generated `id`. Do not send `id` when creating a category.

### Product fields

When creating or updating a product (`POST /products` or `PUT /products/{id}`), send a JSON body with:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | yes | Product name (cannot be empty or whitespace-only) |
| `unit` | string | yes | Unit of measure — must be one of: `each`, `lb`, `kg`, `bag`, `box` |
| `cost_per_unit` | number | yes | Cost per unit (must be ≥ 0) |
| `price_per_unit` | number | yes | Selling price per unit (must be > 0) |
| `quantity_in_stock` | number | yes | Current stock quantity (must be ≥ 0) |
| `category_id` | integer | yes | ID of an existing category |

Responses include an auto-generated `id` and a nested `category` object (`id`, `name`). Do not send `id` when creating a product.

Creating a product with a nonexistent `category_id` returns `409 Conflict`.

### Example responses

**POST /categories — 201 Created**

```json
{
  "id": 1,
  "name": "Herbs",
  "products": []
}
```

**GET /categories — 200 OK**

```json
[
  {
    "id": 1,
    "name": "Herbs"
  }
]
```

**GET /categories/{id} — 200 OK**

```json
{
  "id": 1,
  "name": "Herbs",
  "products": [
    {
      "id": 1,
      "name": "Basil Plant",
      "unit": "each",
      "cost_per_unit": 1.70,
      "price_per_unit": 4.99,
      "quantity_in_stock": 50
    }
  ]
}
```

**GET /categories/{id} — 404 Not Found**

```json
{
  "detail": "Category does not exist."
}
```

**POST /products — 201 Created**

```json
{
  "id": 1,
  "name": "Basil Plant",
  "unit": "each",
  "cost_per_unit": 1.70,
  "price_per_unit": 4.99,
  "quantity_in_stock": 50,
  "category": {
    "id": 1,
    "name": "Herbs"
  }
}
```

**POST /products — 409 Conflict** (category not found)

```json
{
  "detail": "Category 9999 does not exist."
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
    "quantity_in_stock": 50,
    "category": {
      "id": 1,
      "name": "Herbs"
    }
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
  "quantity_in_stock": 50,
  "category": {
    "id": 1,
    "name": "Herbs"
  }
}
```

**GET /products/{id} — 404 Not Found**

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
  "quantity_in_stock": 25,
  "category": {
    "id": 1,
    "name": "Herbs"
  }
}
```

**PUT /products/{id} — 404 Not Found**

```json
{
  "detail": "Product does not exist."
}
```

**DELETE /products/{id} — 204 No Content** (empty body)

**DELETE /products/{id} — 404 Not Found**

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

Use [Postman](https://www.postman.com/downloads/) to send requests to the API. Start PostgreSQL, configure your `.env` file, then start the server:

```bash
uvicorn main:app --reload --app-dir src
```

The base URL for all requests is `http://127.0.0.1:8000`.

### Import the API into Postman (optional)

With the server running, you can import all endpoints at once:

1. Open Postman and click **Import**.
2. Choose **Link** and paste: `http://127.0.0.1:8000/openapi.json`
3. Click **Continue**, then **Import**.

Postman will create a collection with every endpoint pre-configured. You can skip the manual steps below if you use this option.

### Manual requests in Postman

Create a new collection (e.g. **Say Center API**) and add the following requests.

#### 1. Database check — `GET /db-check`

| Setting | Value |
|---------|-------|
| Method | `GET` |
| URL | `http://127.0.0.1:8000/db-check` |

Click **Send**. A successful response looks like:

```json
{"status": "connected", "product_count": 0}
```

#### 2. Create a category — `POST /categories`

| Setting | Value |
|---------|-------|
| Method | `POST` |
| URL | `http://127.0.0.1:8000/categories` |
| Body | **raw** → **JSON** |

Body example:

```json
{
  "name": "Herbs"
}
```

Click **Send**. Note the `id` in the response — you will need it when creating products.

#### 3. List categories — `GET /categories`

| Setting | Value |
|---------|-------|
| Method | `GET` |
| URL | `http://127.0.0.1:8000/categories` |

#### 4. Get a category by ID — `GET /categories/{id}`

| Setting | Value |
|---------|-------|
| Method | `GET` |
| URL | `http://127.0.0.1:8000/categories/1` |

Replace `1` with the category ID from **POST /categories**.

#### 5. Create a product — `POST /products`

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
  "quantity_in_stock": 50,
  "category_id": 1
}
```

Replace `category_id` with a valid category ID.

#### 6. List all products — `GET /products`

| Setting | Value |
|---------|-------|
| Method | `GET` |
| URL | `http://127.0.0.1:8000/products` |

#### 7. Get a product by ID — `GET /products/{id}`

| Setting | Value |
|---------|-------|
| Method | `GET` |
| URL | `http://127.0.0.1:8000/products/1` |

Replace `1` with the product ID returned from **POST /products**.

#### 8. Search products — `GET /products/search`

| Setting | Value |
|---------|-------|
| Method | `GET` |
| URL | `http://127.0.0.1:8000/products/search` |

Go to the **Params** tab and add:

| Key | Value | Required |
|-----|-------|----------|
| `name` | `Basil Plant` | yes |
| `unit` | `each` | no |

#### 9. Update a product — `PUT /products/{id}`

| Setting | Value |
|---------|-------|
| Method | `PUT` |
| URL | `http://127.0.0.1:8000/products/1` |
| Body | **raw** → **JSON** |

Use the same JSON body shape as **POST /products**, including `category_id`.

#### 10. Delete a product — `DELETE /products/{id}`

| Setting | Value |
|---------|-------|
| Method | `DELETE` |
| URL | `http://127.0.0.1:8000/products/1` |

A successful response returns `204 No Content`. The product is soft-deleted and will no longer appear in list, get, or search results.

### Suggested workflow

1. Start PostgreSQL and set `DATABASE_URL` in your `.env` file.
2. Start the server with `uvicorn main:app --reload --app-dir src`.
3. Open Postman and import the API from `http://127.0.0.1:8000/openapi.json`, or create the requests manually.
4. Send **GET /db-check** to confirm the database is reachable.
5. Send **POST /categories** to create one or more categories.
6. Send **POST /products** with a valid `category_id` to add products.
7. Send **GET /categories/{id}** to view a category and its nested products.
8. Send **GET /products** and **GET /products/{id}** to confirm products were saved.
9. Send **GET /products/search** with a `name` query param to find a product.
10. Send **PUT /products/{id}** to update a product.
11. Send **DELETE /products/{id}** to soft-delete a product.

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

**Products**

- **`ProductModel`** (`src/product/product_model.py`) — Pydantic schema for create and update request bodies.
- **`ProductRead`** (`src/product/product_read.py`) — Pydantic schema for standalone product responses (includes nested category).
- **`ProductInCategory`** (`src/product/product_in_category.py`) — Pydantic schema for products embedded in category responses.
- **`ProductSQL`** (`src/product/product_sql.py`) — SQLAlchemy model mapped to the `products` table.

**Categories**

- **`CategoryModel`** (`src/category/category_model.py`) — Pydantic schema for create request bodies.
- **`CategoryRead`** (`src/category/category_read.py`) — Pydantic schema for category list responses.
- **`CategoryReadWithProducts`** (`src/category/category_read_w_products.py`) — Pydantic schema for category detail responses with nested products.
- **`CategoryInProduct`** (`src/category/category_in_product.py`) — Pydantic schema for category info embedded in product responses.
- **`CategorySQL`** (`src/category/category_sql.py`) — SQLAlchemy model mapped to the `categories` table.

Route handlers in `src/product/product_router.py` and `src/category/category_router.py` convert between these layers: incoming requests are validated as Pydantic models, persisted as SQLAlchemy models, and returned as read schemas.

### Schema Management

> **Warning:**  
> **On every application startup (development mode), the database schema is _dropped and recreated_ automatically. This means all data will be deleted each time you restart the FastAPI app.**  
> _Don't use this mode in production._

This is handled in the routers (`src/product/product_router.py` and `src/category/category_router.py`) with:

```python
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
```

- **`drop_all()`** removes all existing tables.
- **`create_all()`** recreates them for your current models.

This keeps your schema in sync during development and helps quickly iterate on model changes. Once schema management is updated for production, data will persist across server restarts as intended.

## Contributors

<a href="https://github.com/aoshodi-catalyte/SAY-Center-fastapi-service/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=aoshodi-catalyte/SAY-Center-fastapi-service"/>
</a>
