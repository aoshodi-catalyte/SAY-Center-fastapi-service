# Requirements:

1. Products are saved permanently when added to the system and don't disappear everytime the server restarts.
2. Every product that is in the system gets returned.
3. The product with the matching ID is returned.
4. The prodcut being searched for does not exist in the system and a proper message is returned.
5. The API should return the Pydantic APIProduct model — not the SQLAlchemy SQLProduct — so that the API exposes only intentional, stable fields and neveR leaks internal database structure or ORM detail.
6. Existing products can be updated without needing to delete and recreate the item.
7. Products can be permanently removed from the database.
8. Clear failure responses are shown when a user attempts to update or delete something that does not exist.

## Endpoints

- **POST /products** — create a product  
- **GET /products** — list all products  
- **GET /products/{id}** — fetch a single product
- **PUT /products/{id}** - update a single product
- **Delete /products/{id}** - remove a single product



## Request & Response Bodies



Body example for POST and PUT:

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



### POST /products — 201 Created

```json
{
  "name": "Banana Tree",
  "unit": "12 kg",
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
    "name": "Banana Tree",
    "unit": "12 kg",
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
  "name": "Banana Tree",
  "unit": "12 kg",
  "cost_per_unit": 1.23,
  "price_per_unit": 2.50,
  "quantity_in_stock": 100
}
```



### GET /products/{id} — 404 Not Found

```json
{
  "detail": "Product does not exist"
}
```


Update Endpoint
### PUT /products/{id} — 200 OK

```json
{
  "id": 1,
  "name": "Apple Tree",
  "unit": "10 kg",
  "cost_per_unit": 2.25,
  "price_per_unit": 3.50,
  "quantity_in_stock": 80
}
```

### PUT /products/{id} — 404 Not Found

```json
{
  "detail": "Product does not exist"
}
```

Delete Endpoint
### Delete /products/{id} — 204 No Content


```json



```

### Delete /products/{id} — 404 Not Found

```json
{
  "detail": "Product does not exist"
}
```



### Pydantic schemas — validate request data and define response shapes
  -Name validation
  -Unit validation
  -Negative numbers validation


### SQLAlchemy models — define DB tables and handle persistence



### Route functions — orchestrate validation, DB operations, and return responses



## Product fields returned:
- id
- name
- unit
- cost_per_unit
- price_per_unit
- quantity_in_stock

## so the client can:

- confirm exactly what was saved
- reference the product later using its id
- see inventory and pricing values immediately

# Category Model(SQL):

```
name 
category id
products
```

## Category Model(Pydantic):

```
name
```

## Cateogtry Response(Pydantic):

```
name
category id
```

## Product Model (SQL):

```
updated to have column category id (foreign key owned by product)
```

# End Points:

POST /categories

POST /products

GET /categories/{id}

## Example Request Body for posting new prdouct:

```json
{
  "name": "Basil Plant",
  "unit": "each",
  "cost_per_unit": 1.70,
  "price_per_unit": 4.99,
  "quantity_in_stock": 50,
  "category_id": 3
}
```

## Get Category Response:

Code 200

```json
{
  "id": 3,
  "name": "Herbs",
  "products": [
    {
      "id": 1,
      "name": "Basil Plant",
      "unit": "each",
      "cost_per_unit": 1.70,
      "price_per_unit": 4.99,
      "quantity_in_stock": 50
    },
    {
      "id": 2,
      "name": "Mint Plant",
      "unit": "each",
      "cost_per_unit": 0.50,
      "price_per_unit": 1.00,
      "quantity_in_stock": 40
    }
  ]
}


## Failed post response for category:
code 404 
```json
{
  "detail": "Category not found"
}

```

we do need two schemas:

ProductRead — used when returning a product on its own

ProductInCategory — used when embedding products inside a category response

CategoryReadWithProducts — includes nested products

Because:

The standalone product response includes category_id.

The nested version does not need category_id because the parent category already defines it.