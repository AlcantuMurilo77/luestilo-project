import pytest
from sqlalchemy.exc import IntegrityError
from models.models import OrderProduct, Order, Product, Client, ProductCategory, ProductSection
from repositories.order_product_repository import OrderProductRepository
from repositories.order_repository import OrderRepository
from repositories.product_repository import ProductRepository
from repositories.client_repository import ClientRepository

@pytest.fixture
def order_product_repo(db):
    return OrderProductRepository(session=db)

@pytest.fixture
def client_repo(db):
    return ClientRepository(session=db)

@pytest.fixture
def product_repo(db):
    return ProductRepository(session=db)

@pytest.fixture
def order_repo(db):
    return OrderRepository(session=db)

@pytest.fixture
def client(client_repo):
    client = Client(name="Cliente OP", email="clienteop@example.com", cpf="888.888.888-88")
    client_repo.create(client)
    client_repo.session.commit()
    return client

@pytest.fixture
def product(product_repo):
    category = ProductCategory(name="Categoria Teste")
    section = ProductSection(name="Seção Teste")
    product_repo.session.add_all([category, section])
    product_repo.session.commit()

    product = Product(
        name="Produto Teste",
        category_id=category.id,
        section_id=section.id,
        selling_price=9.99,
        initial_stock=100
    )
    product_repo.create(product)
    product_repo.session.commit()
    return product

@pytest.fixture
def order(order_repo, client):
    order = Order(client_id=client.id, status="pending")
    order_repo.create(order)
    order_repo.session.commit()
    return order

def test_create_order_product(order_product_repo, order, product):
    op = OrderProduct(order_id=order.id, product_id=product.id, quantity=3, unit_price=9.99)
    created = order_product_repo.create(op)
    assert created.id is not None
    assert created.quantity == 3

def test_create_invalid_order_product(order_product_repo, product):
    op = OrderProduct(order_id=None, product_id=product.id, quantity=1, unit_price=5.0)
    with pytest.raises(IntegrityError):
        order_product_repo.create(op)
    order_product_repo.session.rollback()

def test_get_order_product(order_product_repo, order, product):
    op = OrderProduct(order_id=order.id, product_id=product.id, quantity=2, unit_price=10.0)
    created = order_product_repo.create(op)
    found = order_product_repo.get(created.id)
    assert found is not None
    assert found.id == created.id

def test_get_all_order_products(order_product_repo, order, product):
    order_product_repo.session.query(OrderProduct).delete()
    order_product_repo.session.commit()

    for i in range(2):
        op = OrderProduct(order_id=order.id, product_id=product.id, quantity=i+1, unit_price=5.0)
        order_product_repo.create(op)
    order_product_repo.session.commit()

    all_ops = order_product_repo.get_all()
    assert len(all_ops) == 2

def test_update_order_product(order_product_repo, order, product):
    op = OrderProduct(order_id=order.id, product_id=product.id, quantity=1, unit_price=10.0)
    created = order_product_repo.create(op)

    updated = order_product_repo.update(created, {"quantity": 5, "unit_price": 8.5})
    assert updated.quantity == 5
    assert updated.unit_price == 8.5

def test_update_by_id_order_product(order_product_repo, order, product):
    op = OrderProduct(order_id=order.id, product_id=product.id, quantity=1, unit_price=10.0)
    created = order_product_repo.create(op)

    updated = order_product_repo.update_by_id(created.id, {"quantity": 7})
    assert updated.quantity == 7

def test_update_nonexistent_order_product(order_product_repo):
    fake = OrderProduct(id=9999, order_id=1, product_id=1, quantity=1, unit_price=1.0)
    with pytest.raises(Exception):
        order_product_repo.update(fake, {"quantity": 10})

def test_update_by_id_nonexistent_order_product(order_product_repo):
    with pytest.raises(ValueError):
        order_product_repo.update_by_id(9999, {"quantity": 10})

def test_delete_order_product(order_product_repo, order, product):
    op = OrderProduct(order_id=order.id, product_id=product.id, quantity=1, unit_price=10.0)
    created = order_product_repo.create(op)
    order_product_repo.delete(created)
    assert order_product_repo.get(created.id) is None
