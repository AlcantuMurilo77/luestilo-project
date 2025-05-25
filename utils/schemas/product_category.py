from pydantic import BaseModel, Field

class ProductCategoryCreate(BaseModel):
    name: str = Field(..., min_length=3, 
                      max_length=60)

class ProductCategoryRead(BaseModel):
    id: int
    name: set

    class Config:
        orm_mode = True
