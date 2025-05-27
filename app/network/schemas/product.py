from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime

from app.network.schemas.product_category import ProductCategoryRead
from app.network.schemas.product_section import ProductSectionRead


class ProductCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=60, example="Milk")
    category_id: int = Field(..., example=1)
    section_id: int = Field(..., example=2)
    selling_price: float = Field(..., example=5.99)
    initial_stock: int = Field(..., example=100)
    cost: Optional[float] = Field(None, example=3.50)
    availability: Optional[bool] = Field(True, example=True)
    description: Optional[str] = Field(None, example="Fresh milk from farm")
    bar_code: Optional[str] = Field(None, max_length=100, example="1234567890123")
    expiration_date: Optional[datetime] = Field(None, example="2025-12-31T00:00:00")
    images: Optional[str] = Field(None, example="http://example.com/image.png")


class ProductRead(BaseModel):
    id: int = Field(..., example=10)
    name: str = Field(..., example="Milk")
    category_id: int = Field(..., example=1)
    section_id: int = Field(..., example=2)
    selling_price: float = Field(..., example=5.99)
    initial_stock: int = Field(..., example=100)
    cost: Optional[float] = Field(None, example=3.50)
    availability: bool = Field(..., example=True)
    description: Optional[str] = Field(None, example="Fresh milk from farm")
    bar_code: Optional[str] = Field(None, example="1234567890123")
    expiration_date: Optional[datetime] = Field(None, example="2025-12-31T00:00:00")
    images: Optional[str] = Field(None, example="http://example.com/image.png")

    category: ProductCategoryRead
    section: ProductSectionRead

    model_config = ConfigDict(from_attributes=True)

class ProductUpdate(ProductCreate):
    pass
