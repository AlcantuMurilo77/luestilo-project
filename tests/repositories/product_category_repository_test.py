import pytest
from sqlalchemy.exc import IntegrityError
from models.models import ProductCategory
from repositories.product_category_repository import ProductCategoryRepository

@pytest.fixture
def category_repo(db):
    return ProductCategoryRepository(session=db)

def test_create_category(category_repo):
    category = ProductCategory(name="Categoria Teste")
    created = category_repo.create(category)
    assert created.id is not None
    assert created.name == "Categoria Teste"

def test_create_duplicate_category_name(category_repo):
    category_repo.create(ProductCategory(name="Duplicada"))
    with pytest.raises(IntegrityError):
        category_repo.create(ProductCategory(name="Duplicada"))
    category_repo.session.rollback()

def test_get_category_by_id(category_repo):
    category = ProductCategory(name="Categoria A")
    created = category_repo.create(category)
    found = category_repo.get(created.id)
    assert found is not None
    assert found.id == created.id
    assert found.name == "Categoria A"

def test_get_all_categories(category_repo):
    category_repo.session.query(ProductCategory).delete()
    category_repo.session.commit()

    nomes = ["Categoria 1", "Categoria 2"]
    for nome in nomes:
        category_repo.create(ProductCategory(name=nome))
    category_repo.session.commit()

    all_categories = category_repo.get_all()
    all_names = [c.name for c in all_categories]
    for nome in nomes:
        assert nome in all_names

def test_update_category(category_repo):
    category = ProductCategory(name="Categoria Original")
    created = category_repo.create(category)

    updated = category_repo.update(created, {"name": "Categoria Atualizada"})
    assert updated.name == "Categoria Atualizada"
    assert updated.id == created.id

def test_delete_category(category_repo):
    category = ProductCategory(name="Categoria Deletar")
    created = category_repo.create(category)
    category_repo.delete(created)

    assert category_repo.get(created.id) is None
