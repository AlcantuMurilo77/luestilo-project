from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Annotated
from datetime import datetime
from app.network.schemas.client import ClientRead
from app.network.schemas.order_product import OrderProductRead

class OrderProductCreate(BaseModel):
    product_id: int = Field(..., example=456)
    quantity: Annotated[int, Field(gt=0, example=3)]
    unit_price: Annotated[float, Field(gt=0, example=29.99)]

    model_config = ConfigDict(from_attributes=True)

class OrderCreate(BaseModel):
    client_id: int = Field(..., example=123)
    status: Optional[str] = Field("pending", example="pending")
    products: List[OrderProductCreate] = Field(..., example=[
        {"product_id": 456, "quantity": 3, "unit_price": 29.99},
        {"product_id": 789, "quantity": 1, "unit_price": 49.99},
    ])

    model_config = ConfigDict(from_attributes=True)

class OrderUpdate(BaseModel):
    client_id: Optional[int]
    status: Optional[str]
    products: Optional[List[OrderProductCreate]]

    model_config = ConfigDict(from_attributes=True)

class OrderRead(BaseModel):
    id: int = Field(..., example=1)
    client_id: int = Field(..., example=123)
    status: str = Field(..., example="pending")
    created_at: datetime = Field(..., example="2024-01-01T12:00:00Z")
    updated_at: datetime = Field(..., example="2024-01-01T13:00:00Z")

    client: ClientRead
    products: List[OrderProductRead]

    model_config = ConfigDict(from_attributes=True)
