# Requirements:

1.  Products are saved permanently when added to the system and don't disappear everytime the server restarts
2.  Every product that is in the system gets returned
3.  The product with the matching ID is returned
4.  The prodcut being searched for does not exist in the system and a proper message is returned. 
5.  The API should return the Pydantic APIProduct model — not the SQLAlchemy SQLProduct — so that the API exposes only intentional, stable fields and neveR leaks internal database structure or ORM detail.

## Endpoints

- **POST /products** — create a product  
- **GET /products** — list all products  
- **GET /products/{id}** — fetch a single product

## Request & Response Bodies

### POST /products — 201 Created
```json
{
  "name": "string",
  "unit": "string",
  "cost_per_unit": 1.23,
  "price_per_unit": 2.50,
  "quantity_in_stock": 100
}
```

### GET /products — 200 OK
```json
[
  {
    "id": 1,
    "name": "string",
    "unit": "string",
    "cost_per_unit": 1.23,
    "price_per_unit": 2.50,
    "quantity_in_stock": 100
  }
]
```

### GET /products/{id} — 200 OK
```json
{
  "id": 1,
  "name": "string",
  "unit": "string",
  "cost_per_unit": 1.23,
  "price_per_unit": 2.50,
  "quantity_in_stock": 100
}
```

### GET /products/{id} — 404 Not Found
```json
{
  "detail": "Product not found"
}
```

### Pydantic schemas — validate request data and define response shapes


### SQLAlchemy models — define DB tables and handle persistence


### Route functions — orchestrate validation, DB operations, and return responses


## All product fields are returned so the client can:

- confirm exactly what was saved
- reference the product later using its id
- see inventory and pricing values immediately

