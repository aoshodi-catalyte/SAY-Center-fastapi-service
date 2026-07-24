from sqlalchemy import Column, Integer, String, Float
from database import Base
from pydantic import BaseModel, Field
from typing import Optional


class APIProduct(BaseModel):
    id: Optional[int] = None
    name: str
    unit: str
    cost_per_unit: float = Field(ge=0)
    price_per_unit: float = Field(ge=0)
    quantity_in_stock: float = Field(ge=0)


class SQLProduct(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    unit = Column(String)
    cost_per_unit = Column(Float)
    price_per_unit = Column(Float)
    quantity_in_stock = Column(Float)
