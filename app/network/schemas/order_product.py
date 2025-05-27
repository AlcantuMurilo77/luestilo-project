from pydantic import BaseModel, ConfigDict, Field
from app.network.schemas.product import ProductRead

class OrderProductCreate(BaseModel):
    order_id: int = Field(..., example=123)
    product_id: int = Field(..., example=456)
    quantity: int = Field(..., example=2)
    unit_price: float = Field(..., example=19.99)

class OrderProductRead(BaseModel):
    id: int = Field(..., example=1)
    order_id: int = Field(..., example=123)
    product_id: int = Field(..., example=456)
    quantity: int = Field(..., example=2)
    unit_price: float = Field(..., example=19.99)

    product: ProductRead

    model_config = ConfigDict(from_attributes=True)
