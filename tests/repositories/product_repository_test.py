import pytest
from models.models import ProductCategory, ProductSection
from repositories.product_repository import ProductRepository
from repositories.product_category_repository import ProductCategoryRepository
from repositories.product_section_repository import ProductSectionRepository
from app.network.schemas.product import ProductCreate
from dotenv import load_dotenv
load_dotenv(".env.test", override=True)

@pytest.fixture
def product_repo(db):
    return ProductRepository(session=db)

@pytest.fixture
def category_repo(db):
    return ProductCategoryRepository(session=db)

@pytest.fixture
def section_repo(db):
    return ProductSectionRepository(session=db)

@pytest.fixture
def category(category_repo):
    cat = category_repo.create(ProductCategory(name="Category Product"))
    return cat

@pytest.fixture
def section(section_repo):
    sec = section_repo.create(ProductSection(name="Section Product"))
    return sec

def test_product_create(product_repo, category, section):
    product_data = ProductCreate(
        name="Product Teste",
        category_id=category.id,
        section_id=section.id,
        cost=10.0,
        selling_price=20.0,
        availability=True,
        description="Product Test Description",
        bar_code="123456789",
        initial_stock=5,
        expiration_date=None,
        images=None
    )
    created = product_repo.create(product_data)
    assert created.id is not None
    assert created.name == "Product Teste"
    assert created.category_id == category.id
    assert created.section_id == section.id

def test_product_create_without_category(product_repo, section):
    product_data = ProductCreate(
        name="Product No Category",
        category_id=9999,
        section_id=section.id,
        cost=10.0,
        selling_price=20.0,
        availability=True,
        description=None,
        bar_code=None,
        initial_stock=5,
        expiration_date=None,
        images=None
    )
    with pytest.raises(ValueError):
        product_repo.create(product_data)

def test_product_create_without_section(product_repo, category):
    product_data = ProductCreate(
        name="Product No Section",
        category_id=category.id,
        section_id=9999,
        cost=10.0,
        selling_price=20.0,
        availability=True,
        description=None,
        bar_code=None,
        initial_stock=5,
        expiration_date=None,
        images=None
    )
    with pytest.raises(ValueError):
        product_repo.create(product_data)

def test_product_get(product_repo, category, section):
    product_data = ProductCreate(
        name="Product Get",
        category_id=category.id,
        section_id=section.id,
        cost=15.0,
        selling_price=30.0,
        availability=True,
        description="Desc get",
        bar_code="987654321",
        initial_stock=10,
        expiration_date=None,
        images=None
    )
    created = product_repo.create(product_data)
    found = product_repo.get(created.id)
    assert found is not None
    assert found.id == created.id
    assert found.name == "Product Get"

def test_product_get_all(product_repo, category, section):
    for p in product_repo.get_all():
        product_repo.delete(p)
    product_repo.session.commit()

    products = [
        ProductCreate(name="Prod1", category_id=category.id, section_id=section.id, cost=5, selling_price=10, availability=True, initial_stock=2, description=None, bar_code=None, expiration_date=None, images=None),
        ProductCreate(name="Prod2", category_id=category.id, section_id=section.id, cost=6, selling_price=12, availability=True, initial_stock=3, description=None, bar_code=None, expiration_date=None, images=None),
    ]
    for p in products:
        product_repo.create(p)
    product_repo.session.commit()

    all_products = product_repo.get_all()
    names = [p.name for p in all_products]
    assert "Prod1" in names
    assert "Prod2" in names

def test_product_update(product_repo, category, section):
    product_data = ProductCreate(
        name="Product Update",
        category_id=category.id,
        section_id=section.id,
        cost=10.0,
        selling_price=20.0,
        availability=True,
        description=None,
        bar_code=None,
        initial_stock=5,
        expiration_date=None,
        images=None
    )
    created = product_repo.create(product_data)

    update_data = {"name": "Product Updated", "cost": 15.0}
    updated = product_repo.update(created.id, update_data)

    assert updated.name == "Product Updated"
    assert updated.cost == 15.0
    assert updated.id == created.id

def test_product_delete(product_repo, category, section):
    product_data = ProductCreate(
        name="Product Delete",
        category_id=category.id,
        section_id=section.id,
        cost=10.0,
        selling_price=20.0,
        availability=True,
        description=None,
        bar_code=None,
        initial_stock=5,
        expiration_date=None,
        images=None
    )
    created = product_repo.create(product_data)
    product_id = created.id

    product_repo.delete(created)
    deleted = product_repo.get(product_id)
    assert deleted is None

def test_product_list_filters(product_repo, category, section):
    for p in product_repo.get_all():
        product_repo.delete(p)
    product_repo.session.commit()

    products = [
        ProductCreate(name="Prod1", category_id=category.id, section_id=section.id, cost=5, selling_price=10, availability=True, initial_stock=2, description=None, bar_code=None, expiration_date=None, images=None),
        ProductCreate(name="Prod2", category_id=category.id, section_id=section.id, cost=6, selling_price=20, availability=False, initial_stock=3, description=None, bar_code=None, expiration_date=None, images=None),
        ProductCreate(name="Prod3", category_id=category.id, section_id=section.id, cost=7, selling_price=30, availability=True, initial_stock=1, description=None, bar_code=None, expiration_date=None, images=None),
    ]
    for p in products:
        product_repo.create(p)
    product_repo.session.commit()

    filtered_min = product_repo.list(price_min=15)
    assert all(p.selling_price >= 15 for p in filtered_min)
    assert any(p.name == "Prod2" for p in filtered_min)
    assert any(p.name == "Prod3" for p in filtered_min)

    filtered_max = product_repo.list(price_max=15)
    assert all(p.selling_price <= 15 for p in filtered_max)
    assert any(p.name == "Prod1" for p in filtered_max)

    filtered_cat = product_repo.list(category_name="Category")
    assert all(p.category_id == category.id for p in filtered_cat)

    filtered_avail = product_repo.list(available=True)
    assert all(p.availability is True for p in filtered_avail)
    assert any(p.name == "Prod1" for p in filtered_avail)
    assert any(p.name == "Prod3" for p in filtered_avail)

    filtered_avail_false = product_repo.list(available=False)
    assert all(p.availability is False for p in filtered_avail_false)
    assert any(p.name == "Prod2" for p in filtered_avail_false)
