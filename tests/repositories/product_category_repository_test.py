import pytest
from sqlalchemy.exc import IntegrityError
from models.models import ProductCategory
from repositories.product_category_repository import ProductCategoryRepository

@pytest.fixture
def category_repo(db):
    return ProductCategoryRepository(session=db)

def test_category_create(category_repo):
    category = ProductCategory(name="Category Test")
    created = category_repo.create(category)
    assert created.id is not None
    assert created.name == "Category Test"

def test_category_create_duplicate_name(category_repo):
    category1 = ProductCategory(name="Duplicated")
    category_repo.create(category1)

    category2 = ProductCategory(name="Duplicated")
    with pytest.raises(IntegrityError):
        category_repo.create(category2)
    category_repo.session.rollback()

def test_category_get(category_repo):
    category = ProductCategory(name="Category 1")
    category_repo.create(category)
    found = category_repo.get(category.id)
    assert found is not None
    assert found.id == category.id
    assert found.name == "Category 1"

def test_category_get_all(category_repo):

    for c in category_repo.get_all():
        category_repo.delete(c)
    category_repo.session.commit()

    categories = [
        ProductCategory(name="Cat1"),
        ProductCategory(name="Cat2"),
    ]
    for c in categories:
        category_repo.create(c)
    category_repo.session.commit()

    all_categories = category_repo.get_all()
    names = [c.name for c in all_categories]
    assert "Cat1" in names
    assert "Cat2" in names

def test_category_update(category_repo):
    category = ProductCategory(name="Category Test")
    created = category_repo.create(category)

    update_data = {"name": "Category Updated"}
    updated = category_repo.update(created, update_data)

    assert updated.name == "Category Updated"
    assert updated.id == created.id

def test_category_delete(category_repo):
    category = ProductCategory(name="Category Delete")
    category_repo.create(category)
    category_id = category.id

    category_repo.delete(category)

    deleted = category_repo.get(category_id)
    assert deleted is None
