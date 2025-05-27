import pytest
from fastapi import status
from app import main
from utils.database import override_get_db
from repositories.order_repository import OrderRepository
from models.models import Order  # Ajuste se o modelo tiver outro nome

@pytest.fixture
def order_repo(session):
    return OrderRepository(session)

def test_list_orders(order_repo):
    main.dependency_overrides[override_get_db] = lambda: order_repo.session

    # Criar alguns pedidos para listar
    order_repo.create(Order(product_id=1, quantity=2, price=100))
    order_repo.create(Order(product_id=2, quantity=1, price=50))

    response = main.test_client().get("/orders/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2

def test_create_order(order_repo):
    main.dependency_overrides[override_get_db] = lambda: order_repo.session

    payload = {
        "product_id": 1,
        "quantity": 3,
        "price": 150.0
    }

    response = main.test_client().post("/orders/", json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["product_id"] == payload["product_id"]
    assert data["quantity"] == payload["quantity"]
    assert data["price"] == payload["price"]

def test_create_order_invalid(order_repo):
    main.dependency_overrides[override_get_db] = lambda: order_repo.session

    # Supondo que um valor inválido (ex: quantity negativa) gere ValueError e 400
    payload = {
        "product_id": 1,
        "quantity": -5,
        "price": 150.0
    }

    response = main.test_client().post("/orders/", json=payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST

def test_get_order(order_repo):
    main.dependency_overrides[override_get_db] = lambda: order_repo.session

    order = order_repo.create(Order(product_id=1, quantity=2, price=100))
    response = main.test_client().get(f"/orders/{order.id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == order.id

def test_get_order_not_found(order_repo):
    main.dependency_overrides[override_get_db] = lambda: order_repo.session

    response = main.test_client().get("/orders/999999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Produto não encontrado"

def test_update_order(order_repo):
    main.dependency_overrides[override_get_db] = lambda: order_repo.session

    order = order_repo.create(Order(product_id=1, quantity=2, price=100))
    payload = {
        "product_id": 1,
        "quantity": 5,
        "price": 120.0
    }

    response = main.test_client().put(f"/orders/{order.id}", json=payload)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["quantity"] == payload["quantity"]
    assert data["price"] == payload["price"]

def test_update_order_not_found(order_repo):
    main.dependency_overrides[override_get_db] = lambda: order_repo.session

    payload = {
        "product_id": 1,
        "quantity": 5,
        "price": 120.0
    }

    response = main.test_client().put("/orders/999999", json=payload)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Produto não encontrado"

def test_delete_order(order_repo):
    main.dependency_overrides[override_get_db] = lambda: order_repo.session

    order = order_repo.create(Order(product_id=1, quantity=2, price=100))

    response = main.test_client().delete(f"/orders/{order.id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

def test_delete_order_not_found(order_repo):
    main.dependency_overrides[override_get_db] = lambda: order_repo.session

    response = main.test_client().delete("/orders/999999")
    # delete pode ser idempotente, dependendo da sua implementação
    assert response.status_code in (status.HTTP_204_NO_CONTENT, status.HTTP_404_NOT_FOUND)
