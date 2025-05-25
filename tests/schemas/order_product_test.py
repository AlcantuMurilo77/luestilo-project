import pytest
from pydantic import ValidationError
from utils.schemas.order_product import OrderProductCreate

def test_valid_order_product_create():
    item = OrderProductCreate(order_id=1, 
                              product_id=1, 
                              quantity=2, 
                              unit_price=10.0)
    assert item.quantity == 2

def test_invalid_quantity():
    with pytest.raises(ValidationError):
        OrderProductCreate(order_id=1, 
                           product_id=1, 
                           quantity="two", 
                           unit_price=10.0)
