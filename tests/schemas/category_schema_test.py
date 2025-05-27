import pytest
from pydantic import ValidationError
from app.network.schemas.product_category import ProductCategoryCreate

def test_valid_category_create():
    category = ProductCategoryCreate(name="Food")
    assert category.name == "Food"

def test_invalid_category_name():
    with pytest.raises(ValidationError):
        ProductCategoryCreate(name="")  
