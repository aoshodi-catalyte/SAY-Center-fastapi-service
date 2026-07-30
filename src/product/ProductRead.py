from pydantic import BaseModel, Field


class ProductResponse(BaseModel):
    """Pydantic schema for product responses returned by the API."""

    id: int = Field(default=None, description="Auto-generated product ID.")
    name: str = Field(description="Display name of the product.")
    unit: str = Field(description='Unit of measure, e.g. "kg" or "each".')
    cost_per_unit: float = Field(ge=0, description="Purchase cost per unit.")
    price_per_unit: float = Field(ge=0, description="Selling price per unit.")
    quantity_in_stock: float = Field(ge=0, description="Current stock quantity.")
