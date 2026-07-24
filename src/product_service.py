from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session
from product.product_repository import ProductRepository
from product.models import APIProduct, SQLProduct
from database import Base, engine, SessionLocal

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

app = FastAPI()
product_repo = ProductRepository()


@app.get("/")
def home_page():
    return {"message": "Hello!"}


@app.post("/products", status_code=201)
def post_product(product: APIProduct):
    saved = product_repo.add_product(product)
    return saved


@app.get("/products")
def get_products():
    return [p.model_dump() for p in product_repo.get_all_products()]


@app.get("/products/search")
def search_products(name: str, unit: str | None = None):
    products = product_repo.get_all_products()

    matching = [
        p.model_dump()
        for p in products
        if p.name == name and (unit is None or p.unit == unit)
    ]

    return matching


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/db-check")
def db_check(db: Session = Depends(get_db)):
    try:
        count = db.query(SQLProduct).count()
        return {"status": "connected", "product_count": count}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database connection failed: {str(e)}",
        )
