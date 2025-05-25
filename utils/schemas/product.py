from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime


class ProductCreate(BaseModel):
    name:str = Field(min_length=3, max_length=60)
    category_id: int
    section_id: int
    selling_price: float
    initial_stock: int
    cost: Optional[float] = None
    availability: Optional[bool] = True
    description: Optional[str] = None
    bar_code: Optional[str] = Field(None, max_length=100)
    expiration_date: Optional[datetime] = None
    images: Optional[str] = None
