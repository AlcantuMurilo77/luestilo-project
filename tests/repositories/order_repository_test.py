import pytest
from models.models import Product, ProductCategory, ProductSection
from repositories.order_repository import OrderRepository
from repositories.client_repository import ClientRepository
from repositories.product_repository import ProductRepository
from repositories.product_category_repository import ProductCategoryRepository
from repositories.product_section_repository import ProductSectionRepository
from app.network.schemas.order import OrderCreate, OrderUpdate
from app.network.schemas.order_product import OrderProductCreate
from dotenv import load_dotenv
load_dotenv(".env.test", override=True)

@pytest.fixture
def order_repo(db):
    return OrderRepository(session=db)

@pytest.fixture
def client_repo(db):
    return ClientRepository(session=db)

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
def client(client_repo):
    return client_repo.create(name="Cliente Order", email="clienteorder@example.com", cpf="777.777.777-77")

@pytest.fixture
def category(category_repo):
    return category_repo.create(name="Categoria Order")

@pytest.fixture
def section(section_repo):
    return section_repo.create(name="Seção Order")

@pytest.fixture
def product(product_repo, category, section):
    return product_repo.create({
        "name": "Produto Teste",
        "category_id": category.id,
        "section_id": section.id,
        "cost": 10.0,
        "selling_price": 20.0,
        "availability": True,
        "initial_stock": 10,
        "description": None,
        "bar_code": None,
        "expiration_date": None,
        "images": None
    })


def test_order_create(order_repo, client, product):
    order_data = OrderCreate(
        client_id=client.id,
        status="pending",
        products=[
            OrderProductCreate(product_id=product.id, quantity=2, unit_price=20.0)
        ]
    )
    created = order_repo.create(order_data)
    assert created.id is not None
    assert created.client_id == client.id
    assert created.status == "pending"
    assert len(created.products) == 1
    assert created.products[0].product_id == product.id


def test_order_create_invalid_client(order_repo, product):
    order_data = OrderCreate(
        client_id=9999,
        status="pending",
        products=[
            OrderProductCreate(product_id=product.id, quantity=1, unit_price=20.0)
        ]
    )
    with pytest.raises(ValueError):
        order_repo.create(order_data)


def test_order_get(order_repo, client, product):
    order_data = OrderCreate(
        client_id=client.id,
        status="pending",
        products=[OrderProductCreate(product_id=product.id, quantity=1, unit_price=20.0)]
    )
    created = order_repo.create(order_data)
    found = order_repo.get(created.id)
    assert found is not None
    assert found.id == created.id
    assert found.client_id == client.id
    assert found.products[0].product_id == product.id


def test_order_get_all(order_repo, client, product):
    for o in order_repo.get_all():
        order_repo.delete(o)
    order_repo.session.commit()

    orders = [
        OrderCreate(client_id=client.id, status="pending", products=[OrderProductCreate(product_id=product.id, quantity=1, unit_price=10.0)]),
        OrderCreate(client_id=client.id, status="completed", products=[OrderProductCreate(product_id=product.id, quantity=2, unit_price=20.0)]),
    ]
    for o in orders:
        order_repo.create(o)

    all_orders = order_repo.get_all()
    statuses = [o.status for o in all_orders]
    assert "pending" in statuses
    assert "completed" in statuses


def test_order_update(order_repo, client, product):
    order_data = OrderCreate(
        client_id=client.id,
        status="pending",
        products=[OrderProductCreate(product_id=product.id, quantity=1, unit_price=20.0)]
    )
    created = order_repo.create(order_data)

    update_data = OrderUpdate(
        status="completed",
        products=[OrderProductCreate(product_id=product.id, quantity=3, unit_price=25.0)]
    )
    updated = order_repo.update_order(created.id, update_data)

    assert updated.status == "completed"
    assert len(updated.products) == 1
    assert updated.products[0].quantity == 3
    assert updated.products[0].unit_price == 25.0


def test_order_update_nonexistent(order_repo, product):
    update_data = OrderUpdate(
        status="shipped",
        products=[OrderProductCreate(product_id=product.id, quantity=1, unit_price=10.0)]
    )
    updated = order_repo.update_order(9999, update_data)
    assert updated is None


def test_order_delete(order_repo, client, product):
    order_data = OrderCreate(
        client_id=client.id,
        status="pending",
        products=[OrderProductCreate(product_id=product.id, quantity=1, unit_price=20.0)]
    )
    created = order_repo.create(order_data)
    order_id = created.id

    order_repo.delete(created)

    deleted = order_repo.get(order_id)
    assert deleted is None
