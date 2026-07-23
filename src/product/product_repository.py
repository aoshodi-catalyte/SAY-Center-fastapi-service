from .product_model import Product

products = []

class ProductRepository:

    def get_all_products(self):
        return products

    def add_product(self, product: Product):
        products.append(product)
        return product

    def update_product(self, product: Product):
        for i, p in enumerate(products):
            if p.name == product.name:
                products[i] = product
                return product
        return None

    def delete_product(self, name: str):
        for i, p in enumerate(products):
            if p.name == name:
                products.remove(p)
                return p
        return None

    def get_product_by_name(self, name: str):
        for p in products:
            if p.name == name:
                return p
        return None






    