"""In-memory product repository for early development and unit tests."""

from typing import List, Optional

from .product_model import ProductModel


class ProductRepository:
    """Store and retrieve products in an in-memory list.

    This repository is not backed by a database. It is used for testing and
    prototyping before the PostgreSQL-backed service layer is wired in.
    """

    def __init__(self) -> None:
        """Initialize an empty product store."""
        self.products: List[ProductModel] = []

    def get_all_products(self) -> List[ProductModel]:
        """Return every product currently stored in memory."""
        return self.products

    def add_product(self, product: ProductModel) -> ProductModel:
        """Append a product to the in-memory store.

        Args:
            product: Product to add.

        Returns:
            The same product instance that was stored.
        """
        self.products.append(product)
        return product

    def update_product(self, product: ProductModel) -> Optional[ProductModel]:
        """Replace an existing product matched by name.

        Args:
            product: Product with updated field values. Matching is done by
                ``name``.

        Returns:
            The updated product if a match was found, otherwise ``None``.
        """
        for i, p in enumerate(self.products):
            if p.name == product.name:
                self.products[i] = product
                return product
        return None

    def delete_product(self, name: str) -> Optional[ProductModel]:
        """Remove a product from the store by name.

        Args:
            name: Name of the product to delete.

        Returns:
            The removed product if found, otherwise ``None``.
        """
        for i, p in enumerate(self.products):
            if p.name == name:
                self.products.remove(p)
                return p
        return None

    def get_product_by_name(self, name: str) -> Optional[ProductModel]:
        """Look up a single product by its name.

        Args:
            name: Product name to search for.

        Returns:
            The matching product if found, otherwise ``None``.
        """
        for p in self.products:
            if p.name == name:
                return p
        return None
