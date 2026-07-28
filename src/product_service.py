"""FastAPI application for the Say Center product inventory API.

Exposes CRUD endpoints backed by PostgreSQL via SQLAlchemy. Incoming requests
are validated with Pydantic schemas and persisted as ORM models.
"""

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session
from product.APIProduct import APIProduct
from product.SQLSchema import SQLSchema
from product.ProductResponse import ProductResponse
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

app = FastAPI(
    title="Say Center Product Service",
    description="Product inventory API for creating, listing, searching, and managing products.",
)


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


@app.get("/")
def home_page() -> dict[str, str]:
    """Return a welcome message to confirm the service is running."""
    return {"message": "Hello!"}


@app.post(
    "/products", status_code=status.HTTP_201_CREATED, response_model=ProductResponse
)
def post_product(product: APIProduct, db: Session = Depends(get_db)) -> SQLSchema:
    """Create a new product and persist it to the database.

    Args:
        product: Validated product fields from the request body.
        db: Database session injected by FastAPI.

    Returns:
        The newly created product, including its generated ID.
    """
    new_product = SQLSchema(**product.model_dump())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


@app.get("/products", response_model=List[ProductResponse])
def get_products(db: Session = Depends(get_db)) -> list[SQLSchema]:
    """List every product stored in the database."""
    products = db.query(SQLSchema).filter(SQLSchema.active == True).all()
    return products


@app.get("/products/search", response_model=List[ProductResponse])
def search_products(
    name: str, unit: str | None = None, db: Session = Depends(get_db)
) -> list[SQLSchema]:
    """Search products by exact name, with an optional unit filter.

    Args:
        name: Product name to match exactly.
        unit: When provided, only products with this unit are returned.
        db: Database session injected by FastAPI.

    Returns:
        All products matching the given criteria.
    """
    query = db.query(SQLSchema).filter(SQLSchema.name == name)
    if unit:
        query = query.filter(SQLSchema.unit == unit)

    results = query.all()
    return results


@app.get("/db-check", response_model=dict)
def db_check(db: Session = Depends(get_db)) -> dict[str, str | int]:
    """Verify database connectivity and return the current product count.

    Args:
        db: Database session injected by FastAPI.

    Returns:
        A status object with ``status`` and ``product_count`` keys.

    Raises:
        HTTPException: If the database query fails.
    """
    try:
        count = db.query(SQLSchema).count()
        return {"status": "connected", "product_count": count}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database connection failed: {str(e)}",
        )


@app.get("/products/{id}", response_model=ProductResponse)
def get_product_by_id(id: int, db: Session = Depends(get_db)) -> SQLSchema:
    """Fetch a single product by its primary key.

    Args:
        id: Product ID to look up.
        db: Database session injected by FastAPI.

    Returns:
        The matching product record.

    Raises:
        HTTPException: If no product exists with the given ID.
    """
    product = db.query(SQLSchema).filter(SQLSchema.id == id, SQLSchema.active == True).first()

    if product is None:
        raise HTTPException(status_code=404, detail="Product does not exist.")

    return product


@app.put(
    "/products/{id}", response_model=ProductResponse, status_code=status.HTTP_200_OK
)
def update_product(
    id: int, updated: APIProduct, db: Session = Depends(get_db)
) -> SQLSchema:
    """Replace all fields on an existing product.

    Args:
        id: Product ID to update.
        updated: New field values from the request body.
        db: Database session injected by FastAPI.

    Returns:
        The updated product record.

    Raises:
        HTTPException: If no product exists with the given ID.
    """
    product = db.query(SQLSchema).filter(SQLSchema.id == id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product does not exist")

    for field, value in updated.model_dump().items():
        setattr(product, field, value)

    db.commit()
    db.refresh(product)
    return product

@app.delete("/products/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(id: int, db: Session = Depends(get_db)) -> None:
    """Remove a product from the database.

    Args:
        id: Product ID to delete.
        db: Database session injected by FastAPI.

    Raises:
        HTTPException: If no product exists with the given ID.
    """
    product = db.query(SQLSchema).filter(SQLSchema.id == id).first()

    if product is None:
        raise HTTPException(status_code=404, detail="Product does not exist")
    
    product.active = False
    db.commit()

    return None