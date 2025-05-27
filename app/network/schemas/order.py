from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Annotated
from datetime import datetime
from app.network.schemas.client import ClientRead
from app.network.schemas.order_product import OrderProductRead

class OrderProductCreate(BaseModel):
    product_id: int
    quantity: Annotated[int, Field(gt=0)]
    unit_price: Annotated[float, Field(gt=0)]

    model_config = ConfigDict(from_attributes=True)

class OrderCreate(BaseModel):
    client_id: int
    status: Optional[str] = "pending"
    products: List[OrderProductCreate]

    model_config = ConfigDict(from_attributes=True)

class OrderUpdate(BaseModel):
    client_id: Optional[int]
    status: Optional[str]
    products: Optional[List[OrderProductCreate]]

    model_config = ConfigDict(from_attributes=True)

class OrderRead(BaseModel):
    id: int
    client_id: int
    status: str
    created_at: datetime
    updated_at: datetime

    client: ClientRead
    products: List[OrderProductRead]

    model_config = ConfigDict(from_attributes=True)
