from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class OrderCreate(BaseModel):
    client_id: int
    status: Optional[str] = "pending"

class OrderRead(BaseModel):
    id: int
    client_id: int
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        model_config = ConfigDict(from_attributes=True)
