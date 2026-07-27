from itertools import product
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session
from product.models import APIProduct, SQLProduct, ProductResponse
from database import Base, engine, SessionLocal
from typing import List


def create_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


create_db()

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home_page():
    return {"message": "Hello!"}


@app.post(
    "/products", status_code=status.HTTP_201_CREATED, response_model=ProductResponse
)
def post_product(product: APIProduct, db: Session = Depends(get_db)):
    # new_product = Product(name, unit, cost_per_unit, price_per_unit, quantity_in_stock)
    new_product = SQLProduct(**product.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


@app.get("/products", response_model=List[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    products = db.query(SQLProduct).all()
    return products


@app.get("/products/search", response_model=List[ProductResponse])
def search_products(name: str, unit: str | None = None, db: Session = Depends(get_db)):
    query = db.query(SQLProduct).filter(SQLProduct.name == name)
    if unit:
        query = query.filter(SQLProduct.unit == unit)

    results = query.all()
    return results


@app.get("/db-check", response_model=dict)
def db_check(db: Session = Depends(get_db)):
    try:
        count = db.query(SQLProduct).count()
        return {"status": "connected", "product_count": count}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database connection failed: {str(e)}",
        )


@app.get("/products/{id}", response_model=ProductResponse)
def get_product_by_id(id: int, db: Session = Depends(get_db)):
    product = db.query(SQLProduct).filter(SQLProduct.id == id).first()

    if product is None:
        raise HTTPException(status_code=404, detail="Product does not exist.")

    return product

@app.delete("/products/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(id:int, db: Session = Depends(get_db)):
    product = db.query(SQLProduct).filter(SQLProduct.id == id).first()

    if product is None:
        raise HTTPException(status_code=404, detail="Product does not exist")

    db.delete(product)
    db.commit()
    return None