import pytest
from sqlalchemy.exc import IntegrityError
from models.models import Order, Client
from repositories.order_repository import OrderRepository
from repositories.client_repository import ClientRepository

@pytest.fixture
def order_repo(db):
    return OrderRepository(session=db)

@pytest.fixture
def client_repo(db):
    return ClientRepository(session=db)

@pytest.fixture
def client(client_repo):
    c = Client(name="Cliente Order", email="clienteorder@example.com", cpf="777.777.777-77")
    client_repo.create(c)
    client_repo.session.commit()
    return c

def test_order_create(order_repo, client):
    order = Order(client_id=client.id, status="pending")
    created = order_repo.create(order)
    assert created.id is not None
    assert created.client_id == client.id
    assert created.status == "pending"

def test_order_create_without_client(order_repo):
    order = Order(status="pending", client_id=None)
    with pytest.raises(IntegrityError):
        order_repo.create(order)
    order_repo.session.rollback()

def test_order_create_with_nonexistent_client(order_repo):
    order = Order(client_id=9999999, status="pending")
    with pytest.raises(IntegrityError):
        order_repo.create(order)
    order_repo.session.rollback()

def test_order_get(order_repo, client):
    order = Order(client_id=client.id, status="pending")
    order_repo.create(order)
    found = order_repo.get(order.id)
    assert found is not None
    assert found.id == order.id
    assert found.client_id == client.id

def test_order_get_all(order_repo, client):
    for o in order_repo.get_all():
        order_repo.delete(o)
    order_repo.session.commit()

    orders = [
        Order(client_id=client.id, status="pending"),
        Order(client_id=client.id, status="completed"),
    ]
    for o in orders:
        order_repo.create(o)
    order_repo.session.commit()

    all_orders = order_repo.get_all()
    statuses = [o.status for o in all_orders]
    assert "pending" in statuses
    assert "completed" in statuses

def test_order_update(order_repo, client):
    order = Order(client_id=client.id, status="pending")
    created = order_repo.create(order)

    update_data = {"status": "completed"}
    updated = order_repo.update(created, update_data)

    assert updated.status == "completed"
    assert updated.id == created.id

def test_order_update_nonexistent(order_repo):
    fake_order = Order(id=999999, client_id=1, status="pending")
    with pytest.raises(Exception):
        order_repo.update(fake_order, {"status": "completed"})

def test_order_delete(order_repo, client):
    order = Order(client_id=client.id, status="pending")
    order_repo.create(order)
    order_id = order.id

    order_repo.delete(order)

    deleted = order_repo.get(order_id)
    assert deleted is None
