import pytest
from sqlalchemy.exc import IntegrityError
from models.models import Product, ProductCategory, ProductSection
from repositories.product_repository import ProductRepository
from repositories.product_category_repository import ProductCategoryRepository
from repositories.product_section_repository import ProductSectionRepository

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
    cat = ProductCategory(name="Category Product")
    category_repo.create(cat)
    category_repo.session.commit()
    return cat

@pytest.fixture
def section(section_repo):
    sec = ProductSection(name="Section Product")
    section_repo.create(sec)
    section_repo.session.commit()
    return sec

def test_product_create(product_repo, category, section):
    product = Product(
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
        images=None,
    )
    created = product_repo.create(product)
    assert created.id is not None
    assert created.name == "Product Teste"
    assert created.category_id == category.id
    assert created.section_id == section.id

def test_product_create_without_category(product_repo, section):
    product = Product(
        name="Product No Category",
        category_id=None,
        section_id=section.id,
        cost=10.0,
        selling_price=20.0,
        availability=True,
        description=None,
        bar_code=None,
        initial_stock=5,
        expiration_date=None,
        images=None,
    )
    with pytest.raises(IntegrityError):
        product_repo.create(product)
    product_repo.session.rollback()

def test_product_create_without_section(product_repo, category):
    product = Product(
        name="Product No Section",
        category_id=category.id,
        section_id=None,
        cost=10.0,
        selling_price=20.0,
        availability=True,
        description=None,
        bar_code=None,
        initial_stock=5,
        expiration_date=None,
        images=None,
    )
    with pytest.raises(IntegrityError):
        product_repo.create(product)
    product_repo.session.rollback()

def test_product_get(product_repo, category, section):
    product = Product(
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
        images=None,
    )
    product_repo.create(product)
    found = product_repo.get(product.id)
    assert found is not None
    assert found.id == product.id
    assert found.name == "Product Get"

def test_product_get_all(product_repo, category, section):

    for p in product_repo.get_all():
        product_repo.delete(p)
    product_repo.session.commit()

    products = [
        Product(name="Prod1", category_id=category.id, section_id=section.id, cost=5, selling_price=10, initial_stock=2),
        Product(name="Prod2", category_id=category.id, section_id=section.id, cost=6, selling_price=12, initial_stock=3),
    ]
    for p in products:
        product_repo.create(p)
    product_repo.session.commit()

    all_products = product_repo.get_all()
    names = [p.name for p in all_products]
    assert "Prod1" in names
    assert "Prod2" in names

def test_product_update(product_repo, category, section):
    product = Product(
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
        images=None,
    )
    created = product_repo.create(product)

    update_data = {"name": "Product Updated", "cost": 15.0}
    updated = product_repo.update(created, update_data)

    assert updated.name == "Product Updated"
    assert updated.cost == 15.0
    assert updated.id == created.id

def test_product_delete(product_repo, category, section):
    product = Product(
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
        images=None,
    )
    product_repo.create(product)
    product_id = product.id

    product_repo.delete(product)

    deleted = product_repo.get(product_id)
    assert deleted is None

@pytest.mark.asyncio
async def test_product_get_all_with_filters(product_repo, category, section):

    prods = await product_repo.get_all()
    for p in prods:
        await product_repo.delete(p)
    await product_repo.session.commit()


    products = [
        Product(name="Prod1", category_id=category.id, section_id=section.id, cost=5, selling_price=10, availability=True, initial_stock=2),
        Product(name="Prod2", category_id=category.id, section_id=section.id, cost=6, selling_price=20, availability=False, initial_stock=3),
        Product(name="Prod3", category_id=category.id, section_id=section.id, cost=7, selling_price=30, availability=True, initial_stock=1),
    ]
    for p in products:
        await product_repo.create(p)
    await product_repo.session.commit()


    filtered_min = await product_repo.get_all(min_price=15)
    assert all(p.selling_price >= 15 for p in filtered_min)
    assert any(p.name == "Prod2" for p in filtered_min)
    assert any(p.name == "Prod3" for p in filtered_min)
    assert all(p.name != "Prod1" for p in filtered_min)

    filtered_max = await product_repo.get_all(max_price=15)
    assert all(p.selling_price <= 15 for p in filtered_max)
    assert any(p.name == "Prod1" for p in filtered_max)
    assert all(p.name != "Prod2" for p in filtered_max)


    filtered_cat = await product_repo.get_all(category_filter=category.id)
    assert len(filtered_cat) >= 3  
    assert all(p.category_id == category.id for p in filtered_cat)


    filtered_avail = await product_repo.get_all(availability_filter=True)
    assert all(p.availability is True for p in filtered_avail)
    assert any(p.name == "Prod1" for p in filtered_avail)
    assert any(p.name == "Prod3" for p in filtered_avail)
    assert all(p.name != "Prod2" for p in filtered_avail)

    filtered_avail_false = await product_repo.get_all(availability_filter=False)
    assert all(p.availability is False for p in filtered_avail_false)
    assert any(p.name == "Prod2" for p in filtered_avail_false)