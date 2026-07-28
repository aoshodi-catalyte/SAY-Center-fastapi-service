"""Product data models for API validation and database persistence."""

from sqlalchemy import Column, Integer, String, Float
from database import Base
from pydantic import BaseModel, Field
from typing import Optional


class APIProduct(BaseModel):
    """Pydantic schema for product request bodies.

    Used to validate incoming create and update payloads. Clients must not
    send an ``id``; it is assigned by the database.
    """

    name: str = Field(description="Display name of the product.")
    unit: str = Field(description='Unit of measure, e.g. "kg" or "each".')
    cost_per_unit: float = Field(ge=0, description="Purchase cost per unit.")
    price_per_unit: float = Field(ge=0, description="Selling price per unit.")
    quantity_in_stock: float = Field(ge=0, description="Current stock quantity.")


class ProductResponse(BaseModel):
    """Pydantic schema for product responses returned by the API."""

    id: Optional[int] = Field(default=None, description="Auto-generated product ID.")
    name: str = Field(description="Display name of the product.")
    unit: str = Field(description='Unit of measure, e.g. "kg" or "each".')
    cost_per_unit: float = Field(ge=0, description="Purchase cost per unit.")
    price_per_unit: float = Field(ge=0, description="Selling price per unit.")
    quantity_in_stock: float = Field(ge=0, description="Current stock quantity.")


class SQLProduct(Base):
    """SQLAlchemy ORM model mapped to the ``products`` table."""

    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    unit = Column(String)
    cost_per_unit = Column(Float)
    price_per_unit = Column(Float)
    quantity_in_stock = Column(Float)
