from pydantic import BaseModel, Field, ConfigDict

class ProductCategoryCreate(BaseModel):
    name: str = Field(..., min_length=3, 
                      max_length=60)

class ProductCategoryRead(BaseModel):
    id: int
    name: set

    model_config = ConfigDict(from_attributes=True)
