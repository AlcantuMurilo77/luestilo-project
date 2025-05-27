import pytest
from pydantic import ValidationError
from app.network.schemas.product_section import ProductSectionCreate

def test_valid_section_create():
    section = ProductSectionCreate(name="Hygiene")
    assert section.name == "Hygiene"

def test_invalid_section_name():
    with pytest.raises(ValidationError):
        ProductSectionCreate(name="  ")  
