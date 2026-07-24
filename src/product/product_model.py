from pydantic import BaseModel, Field
from typing import Optional


class Product(BaseModel):
    id: Optional[int] = None
    name: str
    unit: str
    cost_per_unit: float = Field(ge=0)
    price_per_unit: float = Field(ge=0)
    quantity_in_stock: float = Field(ge=0)
