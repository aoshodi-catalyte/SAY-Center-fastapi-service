What does the Category model look like, and what does the foreign key on Product look like? Which side owns the foreign key?
What are the exact endpoints (method + path) for creating a category, creating a product that references a category, and retrieving a category with its products?
What does the request body look like for creating a product now that it must reference a category id?
What does a successful "get category with products" response look like — status code and full nested body shape?
What does the failure response look like when a product is created with a category id that doesn't exist — status code and body shape?
What do the Pydantic schemas look like for the nested cases — is there a separate schema for "product as seen inside a category response" versus "product as seen on its own"? Why or why not?
