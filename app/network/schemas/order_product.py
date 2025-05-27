from pydantic import BaseModel, ConfigDict
from app.network.schemas.product import ProductRead

class OrderProductCreate(BaseModel):
    order_id: int
    product_id: int
    quantity: int
    unit_price: float

class OrderProductRead(BaseModel):
    id: int
    order_id: int
    product_id: int
    quantity: int
    unit_price: float

    product: ProductRead

    model_config = ConfigDict(from_attributes=True)
