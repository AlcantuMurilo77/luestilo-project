import pytest
from pydantic import ValidationError
from app.network.schemas.product import ProductCreate
from datetime import datetime

def test_valid_product_creation():
    product = ProductCreate(
        name="Product A",
        category_id=1,
        section_id=1,
        selling_price=9.99,
        initial_stock=10
    )

    assert product.name == "Product A"

def test_missing_required_fields():
    with pytest.raises(ValidationError):
        ProductCreate(name="Product",
                      category_id=1,
                      section_id=1)

def test_invalid_price_type():
    with pytest.raises(ValidationError):
        product = ProductCreate(name="Product A",
                                category_id=1,
                                section_id=1,
                                selling_price="ten",
                                initial_stock=10)
