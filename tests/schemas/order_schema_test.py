import pytest
from pydantic import ValidationError
from app.network.schemas.order import OrderCreate

def test_valid_order_create():
    order = OrderCreate(client_id=1)
    assert order.client_id == 1

def test_missing_client_id():
    with pytest.raises(ValidationError):
        OrderCreate()
