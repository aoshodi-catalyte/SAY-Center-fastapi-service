from pydantic import BaseModel, Field, field_validator
from typing import Optional, Literal

Allowed_Units = ("each", "lb", "kg", "bag", "box")


class APIProduct(BaseModel):
    """Pydantic schema for product request bodies.

    Used to validate incoming create and update payloads. Clients must not
    send an ``id``; it is assigned by the database.
    """

    name: str = Field(description="Display name of the product.")
    unit: str = Field(description='Unit of measure, e.g. "kg" or "each".')
    cost_per_unit: float = Field(ge=0, description="Purchase cost per unit.")
    price_per_unit: float = Field(gt=0, description="Selling price per unit.")
    quantity_in_stock: float = Field(ge=0, description="Current stock quantity.")

    @field_validator("name")
    def validate_name(cls, value):
        if not value.strip():
            raise ValueError("Name cannot be empty")
        return value

    @field_validator("unit")
    def unit_must_be_valid(cls, value):
        if value not in Allowed_Units:
            raise ValueError(f"unit must be one of: {', '.join(Allowed_Units)}")
        return value
