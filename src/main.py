from fastapi import FastAPI
from product_router import router as product_router
from category_router import router as category_router

app = FastAPI()

app.include_router(category_router)
app.include_router(product_router)
