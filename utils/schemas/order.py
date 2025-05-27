from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Annotated
from datetime import datetime

class OrderProductCreate(BaseModel):
    product_id: int
    quantity: Annotated[int, Field(gt=0)]
    unit_price: Annotated[float, Field(gt=0)]

class OrderCreate(BaseModel):
    client_id: int
    status: Optional[str] = "pending"
    products: List[OrderProductCreate]

class OrderUpdate(OrderCreate):
    pass

class OrderRead(BaseModel):
    id: int
    client_id: int
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
