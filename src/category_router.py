"""FastAPI application for the Say Center product inventory API.

Exposes CRUD endpoints backed by PostgreSQL via SQLAlchemy. Incoming requests
are validated with Pydantic schemas and persisted as ORM models.
"""

from sre_parse import CATEGORIES
from sys import prefix
from fastapi import Depends, FastAPI, HTTPException, status, APIRouter
from sqlalchemy.orm import Session, session
from category import category_read_w_products
from category.category_read_w_products import CategoryReadWithProducts
from category.category_read import CategoryRead
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


@router.get("/categories", status_code=200, response_model=list[CategoryRead])
def get_all_categories(db: Session = Depends(get_db)) -> list[CategoryRead]:

    categories = db.query(Category).all()
    return categories

@router.get("/categories/{id}", status_code=200, response_model=CategoryReadWithProducts)
def get_category_by_id(id: int, db: Session = Depends(get_db)) -> CategoryReadWithProducts:
    category = (
        db.query(Category).filter(Category.id).first()
    )

    if category is None:
        raise HTTPException(status_code=404, detail="Category does not exist.")

    return category