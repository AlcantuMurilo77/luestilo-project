from datetime import datetime, timedelta
import pytest
from sqlalchemy.exc import IntegrityError
from models.models import Order, Client, OrderProduct, Product, ProductCategory, ProductSection
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

@pytest.mark.asyncio
async def test_order_get_all_with_filters(
    order_repo, client, db
):
    for o in await order_repo.get_all():
        await order_repo.delete(o)
    await order_repo.session.commit()

    section = ProductSection(name="Seção A")
    db.add(section)
    category = ProductCategory(name="Categoria A")
    db.add(category)
    await db.commit()

    prod1 = Product(name="Produto 1", category_id=category.id, section_id=section.id,
                    cost=5, selling_price=10, initial_stock=5)
    prod2 = Product(name="Produto 2", category_id=category.id, section_id=section.id,
                    cost=7, selling_price=15, initial_stock=3)
    db.add_all([prod1, prod2])
    await db.commit()

    now = datetime.timezone.utc()
    order1 = Order(client_id=client.id, status="pending", created_at=now - timedelta(days=1))
    order2 = Order(client_id=client.id, status="completed", created_at=now)
    db.add_all([order1, order2])
    await db.commit()


    db.add_all([
        OrderProduct(order_id=order1.id, product_id=prod1.id, quantity=1, unit_price=10),
        OrderProduct(order_id=order2.id, product_id=prod2.id, quantity=2, unit_price=15),
    ])
    await db.commit()

    filtered_by_id = await order_repo.get_all(order_id=order1.id)
    assert len(filtered_by_id) == 1
    assert filtered_by_id[0].id == order1.id


    filtered_by_status = await order_repo.get_all(status="completed")
    assert all(o.status == "completed" for o in filtered_by_status)

    filtered_by_client = await order_repo.get_all(client_id=client.id)
    assert all(o.client_id == client.id for o in filtered_by_client)


    filtered_by_start = await order_repo.get_all(start_date=now - timedelta(hours=12))
    assert all(o.created_at >= now - timedelta(hours=12) for o in filtered_by_start)

    filtered_by_end = await order_repo.get_all(end_date=now - timedelta(hours=12))
    assert all(o.created_at <= now - timedelta(hours=12) for o in filtered_by_end)


    filtered_by_section = await order_repo.get_all(section_id=section.id)
    assert all(any(op.product.section_id == section.id for op in o.products) for o in filtered_by_section)