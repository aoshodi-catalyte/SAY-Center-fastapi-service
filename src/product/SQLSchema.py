from sqlalchemy import Boolean, Column, Float, Integer, String
from database import Base


class SQLSchema(Base):
    """SQLAlchemy ORM model mapped to the ``products`` table."""

    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    unit = Column(String)
    cost_per_unit = Column(Float)
    price_per_unit = Column(Float)
    quantity_in_stock = Column(Float)
    active = Column[bool](Boolean, default=True)