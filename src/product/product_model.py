from pydantic import BaseModel

class Product(BaseModel):
    name: str
    unit: str
    cost_per_unit: float
    price_per_unit: float
    quantity_in_stock: float

