"""FastAPI application for the Say Center product inventory API.

Exposes CRUD endpoints backed by PostgreSQL via SQLAlchemy. Incoming requests
are validated with Pydantic schemas and persisted as ORM models.
"""

from sys import prefix
from fastapi import Depends, FastAPI, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from category.categoryRead import CategoryReadWithProducts
from category.category_model import CategoryModel
from category.sql_category import Category
from product.Product_in_category import ProductInCategory
from database import Base, engine, SessionLocal
from typing import Generator, List


def create_db() -> None:
    """Drop and recreate all database tables.

    Used during development to keep the schema in sync with model definitions.
    All existing data is removed on each call.
    """
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


create_db()

router = APIRouter()


def get_db() -> Generator[Session, None, None]:
    """Provide a SQLAlchemy session for the duration of a request.

    Yields:
        A database session that is closed when the request completes.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def home_page() -> dict[str, str]:
    """Return a welcome message to confirm the service is running."""
    return {
        "message": "Hello! You are in Categories. Categories table is currently empty."
    }


@router.post(
    "/categories",
    status_code=status.HTTP_201_CREATED,
    response_model=CategoryReadWithProducts,
)
def post_category(category: CategoryModel, db: Session = Depends(get_db)) -> Category:

    new_category = Category(**category.model_dump())
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category
