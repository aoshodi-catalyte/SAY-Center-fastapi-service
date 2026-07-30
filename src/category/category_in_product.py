from pydantic import BaseModel


class CategoryInProduct(BaseModel):
    id: int
    name: str
