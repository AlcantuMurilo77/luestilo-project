from pydantic import BaseModel, Field, ConfigDict

class ProductCategoryCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=60, example="Beverages")

class ProductCategoryRead(BaseModel):
    id: int = Field(..., example=1)
    name: str = Field(..., example="Beverages")

    model_config = ConfigDict(from_attributes=True)
