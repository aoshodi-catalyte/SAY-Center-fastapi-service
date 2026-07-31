from pydantic import BaseModel, Field, field_validator


class CategoryModel(BaseModel):
    name: str = Field(description="Display name of the category.")

    @field_validator("name")
    def name_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Category name cannot be empty.")
        return v
