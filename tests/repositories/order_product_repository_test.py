import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError
from models.models import OrderProduct, Order, Product, Client
from repositories.order_product_repository import OrderProductRepository
from repositories.order_repository import OrderRepository
from repositories.product_repository import ProductRepository
from repositories.client_repository import ClientRepository

@pytest.fixture
def order_product_repo(db):
    return OrderProductRepository(session=db)

@pytest.fixture
def order_repo(db):
    return OrderRepository(session=db)

@pytest.fixture
def product_repo(db):
    return ProductRepository(session=db)

@pytest.fixture
def client_repo(db):
    return ClientRepository(session=db)

@pytest.fixture
def client(client_repo):
    c = Client(name="Cliente OP", email="clienteop@example.com", cpf="888.888.888-88")
    client_repo.create(c)
    client_repo.session.commit()
    return c

@pytest.fixture
def order(order_repo, client):
    o = Order(client_id=client.id, status="pending")
    order_repo.create(o)
    order_repo.session.commit()
    return o

@pytest.fixture
def product(product_repo):

    from models.models import ProductCategory, ProductSection

    category = ProductCategory(name="Test Category")
    section = ProductSection(name="Test Section")
    product_repo.session.add(category)
    product_repo.session.add(section)
    product_repo.session.commit()

    p = Product(
        name="Test Product",
        category_id=category.id,
        section_id=section.id,
        selling_price=10.0,
        initial_stock=100,
    )
    product_repo.create(p)
    product_repo.session.commit()
    return p

def test_order_product_create(order_product_repo, order, product):
    op = OrderProduct(order_id=order.id, product_id=product.id, quantity=5, unit_price=9.99)
    created = order_product_repo.create(op)
    assert created.id is not None
    assert created.order_id == order.id
    assert created.product_id == product.id
    assert created.quantity == 5
    assert created.unit_price == 9.99

def test_order_product_create_without_order(order_product_repo, product):
    op = OrderProduct(order_id=None, product_id=product.id, quantity=1, unit_price=5.0)
    with pytest.raises(IntegrityError):
        order_product_repo.create(op)
    order_product_repo.session.rollback()

def test_order_product_create_without_product(order_product_repo, order):
    op = OrderProduct(order_id=order.id, product_id=None, quantity=1, unit_price=5.0)
    with pytest.raises(IntegrityError):
        order_product_repo.create(op)
    order_product_repo.session.rollback()

def test_order_product_create_quantity_zero(order_product_repo, order, product):
    op = OrderProduct(order_id=order.id, product_id=product.id, quantity=0, unit_price=5.0)
    with pytest.raises(IntegrityError):
        order_product_repo.create(op)
    order_product_repo.session.rollback()

def test_order_product_create_quantity_negative(order_product_repo, order, product):
    op = OrderProduct(order_id=order.id, product_id=product.id, quantity=-1, unit_price=5.0)
    with pytest.raises(IntegrityError):
        order_product_repo.create(op)
    order_product_repo.session.rollback()

def test_order_product_get(order_product_repo, order, product):
    op = OrderProduct(order_id=order.id, product_id=product.id, quantity=3, unit_price=7.5)
    created = order_product_repo.create(op)
    order_product_repo.session.commit()

    found = order_product_repo.get(created.id)
    assert found is not None
    assert found.id == created.id
    assert found.quantity == 3

def test_order_product_get_all(order_product_repo, order, product):
    for op in order_product_repo.get_all():
        order_product_repo.delete(op)
    order_product_repo.session.commit()

    ops = [
        OrderProduct(order_id=order.id, product_id=product.id, quantity=1, unit_price=5.0),
        OrderProduct(order_id=order.id, product_id=product.id, quantity=2, unit_price=5.0),
    ]
    for o in ops:
        order_product_repo.create(o)
    order_product_repo.session.commit()

    all_ops = order_product_repo.get_all()
    assert len(all_ops) >= 2

def test_order_product_update(order_product_repo, order, product):
    op = OrderProduct(order_id=order.id, product_id=product.id, quantity=1, unit_price=5.0)
    created = order_product_repo.create(op)
    order_product_repo.session.commit()

    update_data = {"quantity": 10, "unit_price": 4.99}
    updated = order_product_repo.update(created, update_data)
    assert updated.quantity == 10
    assert updated.unit_price == 4.99
    assert updated.id == created.id

def test_order_product_update_by_id(order_product_repo, order, product):
    op = OrderProduct(order_id=order.id, product_id=product.id, quantity=1, unit_price=5.0)
    created = order_product_repo.create(op)
    order_product_repo.session.commit()

    updated = order_product_repo.update_by_id(created.id, {"quantity": 20})
    assert updated.quantity == 20
    assert updated.id == created.id

def test_order_product_update_nonexistent(order_product_repo):
    fake_op = OrderProduct(id=999999, order_id=1, product_id=1, quantity=1, unit_price=1.0)
    with pytest.raises(Exception):
        order_product_repo.update(fake_op, {"quantity": 5})

def test_order_product_update_by_id_nonexistent(order_product_repo):
    with pytest.raises(ValueError):
        order_product_repo.update_by_id(999999, {"quantity": 5})

def test_order_product_delete(order_product_repo, order, product):
    op = OrderProduct(order_id=order.id, product_id=product.id, quantity=1, unit_price=5.0)
    created = order_product_repo.create(op)
    order_product_repo.session.commit()

    order_product_repo.delete(created)
    deleted = order_product_repo.get(created.id)
    assert deleted is None
