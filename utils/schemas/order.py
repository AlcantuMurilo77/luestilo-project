from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Annotated
from datetime import datetime

class OrderProductCreate(BaseModel):
    product_id: int = Field(..., example=456)
    quantity: Annotated[int, Field(gt=0, example=3)]
    unit_price: Annotated[float, Field(gt=0, example=29.99)]

class OrderCreate(BaseModel):
    client_id: int = Field(..., example=123)
    status: Optional[str] = Field("pending", example="pending")
    products: List[OrderProductCreate] = Field(..., example=[
        {"product_id": 456, "quantity": 3, "unit_price": 29.99},
        {"product_id": 789, "quantity": 1, "unit_price": 49.99},
    ])

class OrderUpdate(OrderCreate):
    pass

class OrderRead(BaseModel):
    id: int = Field(..., example=1)
    client_id: int = Field(..., example=123)
    status: str = Field(..., example="pending")
    created_at: datetime = Field(..., example="2024-01-01T12:00:00Z")
    updated_at: datetime = Field(..., example="2024-01-01T13:00:00Z")

    model_config = ConfigDict(from_attributes=True)
