from pydantic import BaseModel, Field
from product.Product_in_category import ProductInCategory


class CategoryReadWithProducts(BaseModel):
    id: int = Field(description="Auto-generated category ID.")
    name: str = Field(description="Display name of the category.")
    products: list[ProductInCategory]
