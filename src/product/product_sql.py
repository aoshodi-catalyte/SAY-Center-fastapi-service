from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from database import Base


class ProductSQL(Base):
    """SQLAlchemy ORM model mapped to the ``products`` table."""

    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    unit = Column(String, nullable=False)
    cost_per_unit = Column(Float, nullable=False)
    price_per_unit = Column(Float, nullable=False)
    quantity_in_stock = Column(Float, nullable=False)
    active = Column[bool](Boolean, default=True)

    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)

    category = relationship("CategorySQL", back_populates="products")
