from fastapi import FastAPI
from product.product_repository import ProductRepository
from product.product_model import Product

app = FastAPI()
product_repo = ProductRepository()

@app.get("/")
def home_page():
    return {"message": "Hello!"}

@app.post("/products")
def post_product(product: Product):
    # new_product = Product(name, unit, cost_per_unit, price_per_unit, quantity_in_stock)
    product_repo.add_product(product)
    return {"message": "New Product added successfully!", "product": product}

@app.get("/products")
def get_products():
    return product_repo.get_all_products()

@app.get("/products/search")
def search_products(name: str, unit: str | None = None):
    products = product_repo.get_all_products()

    matching_products = []

    for product in products:
        if product.name == name:
            if unit is None or product.unit == unit:
                matching_products.append(product)

    return matching_products