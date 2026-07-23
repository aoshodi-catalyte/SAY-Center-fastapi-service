from .product_model import Product

class ProductRepository:
    def __init__(self):
        self.products = []

    def get_all_products(self):
        return self.products

    def add_product(self, product: Product):
        self.products.append(product)
        return product

    def update_product(self, product: Product):
        for i, p in enumerate(self.products):
            if p.name == product.name:
                self.products[i] = product
                return product
        return None

    def delete_product(self, name: str):
        for i, p in enumerate(self.products):
            if p.name == name:
                self.products.remove(p)
                return p
        return None

    def get_product_by_name(self, name: str):
        for p in self.products:
            if p.name == name:
                return p
        return None






    