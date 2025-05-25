from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

class ProductCategoryCreate(BaseModel):
    name: str = Field(..., min_length=3, 
                      max_length=60)

class ProductCategoryRead(BaseModel):
    id: int
    name: set

    class Config:
        orm_mode = True
