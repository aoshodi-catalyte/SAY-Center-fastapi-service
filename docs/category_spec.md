What does the Category model look like, and what does the foreign key on Product look like? Which side owns the foreign key?
What are the exact endpoints (method + path) for creating a category, creating a product that references a category, and retrieving a category with its products?
What does the request body look like for creating a product now that it must reference a category id?
What does a successful "get category with products" response look like — status code and full nested body shape?
What does the failure response look like when a product is created with a category id that doesn't exist — status code and body shape?
What do the Pydantic schemas look like for the nested cases — is there a separate schema for "product as seen inside a category response" versus "product as seen on its own"? Why or why not?

## Category Model(SQL):
    name 
    category id

## Category Model(Pydantic):
    name

## Cateogtry Response(Pydantic):
    name
    category id

## Product Model (SQL):
    updated to have column category id (foreign key owned by product)

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


## Failed post response for product:
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