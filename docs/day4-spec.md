What are the exact endpoints (method + path) that satisfy the business requirements above?
What does the request body look like for each, if any?
What does a successful response look like for each — status code and body shape?
What does a failure response look like for requirement 4 — status code and body shape?
Where does validation happen, and where does "talking to the database" happen? (You've now seen Pydantic schemas, SQLAlchemy models, and route functions — how do those three responsibilities get divided?)
What decision did you make about which fields come back in a response, and why?

# Requirements:

1.  Products are saved permanently when added to the system and don't disappear everytime the server restarts
2.  Every product that is in the system gets returned
3.  The product with the matching ID is returned



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

### Pydantic schemas — validate request data and define response shapes


### SQLAlchemy models — define DB tables and handle persistence


### Route functions — orchestrate validation, DB operations, and return responses


## All product fields are returned so the client can:

- confirm exactly what was saved
- reference the product later using its id
- see inventory and pricing values immediately

