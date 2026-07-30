from pydantic import BaseModel, Field


class CategoryModel(BaseModel):
    name: str = Field(description="Display name of the category.")
