"""FastAPI application for the Say Center product inventory API.

Exposes CRUD endpoints backed by PostgreSQL via SQLAlchemy. Incoming requests
are validated with Pydantic schemas and persisted as ORM models.
"""

from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session, with_loader_criteria
from starlette.status import HTTP_200_OK, HTTP_204_NO_CONTENT
from category.category_read_w_products import CategoryReadWithProducts
from category.category_read import CategoryRead
from category.category_model import CategoryModel
from category.category_sql import CategorySQL
from database import Base, engine, SessionLocal
from typing import Generator

from product.product_sql import ProductSQL
from product.product_read import ProductRead


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
def post_category(
    category: CategoryModel, db: Session = Depends(get_db)
) -> CategorySQL:

    new_category = CategorySQL(**category.model_dump())
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category


@router.get("/categories", status_code=200, response_model=list[CategoryRead])
def get_all_categories(db: Session = Depends(get_db)) -> list[CategoryRead]:

    categories = db.query(CategorySQL).all()
    return categories


@router.get(
    "/categories/{id}", status_code=200, response_model=CategoryReadWithProducts
)
def get_category_by_id(id: int, db: Session = Depends(get_db)):
    category = (
        db.query(CategorySQL)
        .options(with_loader_criteria(ProductSQL, ProductSQL.active == True))
        .filter(CategorySQL.id == id)
        .first()
    )

    if category is None:
        raise HTTPException(status_code=404, detail="Category does not exist.")

    return category


@router.get(
    "/categories/{category_id}/{product_name}",
    status_code=200,
    response_model=list[ProductRead],
)
def get_product_by_name_in_category(
    category_id: int,
    product_name: str,
    db: Session = Depends(get_db),
):
    products = (
        db.query(ProductSQL)
        .filter(
            ProductSQL.category_id == category_id,
            ProductSQL.name.ilike(f"%{product_name}%"),
            ProductSQL.active == True,
        )
        .all()
    )

    if products is None:
        raise HTTPException(
            status_code=404, detail="Product not found in this category."
        )

    return products


@router.put(
    "/categories/{id}",
    status_code=HTTP_200_OK,
    response_model=CategoryReadWithProducts,
)
def update_category(
    id: int,
    category_update: CategoryModel,
    db: Session = Depends(get_db),
):
    category = db.query(CategorySQL).filter(CategorySQL.id == id).first()

    if category is None:
        raise HTTPException(status_code=404, detail="Category does not exist.")

    # Pydantic already validated non-empty name
    category.name = category_update.name

    db.commit()
    db.refresh(category)

    return category


@router.delete(
    "/categories/{id}",
    status_code=HTTP_204_NO_CONTENT,
)
def delete_category(id: int, db: Session = Depends(get_db)):
    category = db.query(CategorySQL).filter(CategorySQL.id == id).first()

    if category is None:
        raise HTTPException(status_code=404, detail="Category does not exist.")

    db.delete(category)
    db.commit()

    return {"message": f"Category {id} deleted."}
