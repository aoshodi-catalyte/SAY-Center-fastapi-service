from pydantic import BaseModel, Field


class CategoryRead(BaseModel):
    id: int = Field(description="Auto-generated category ID.")
    name: str = Field(description="Display name of the category.")
