import pytest
from fastapi import status
from app import main
from utils.database import get_db
from repositories.product_repository import ProductRepository
from models.models import Product  

@pytest.fixture
def product_repo(session):
    return ProductRepository(session)

def test_list_products(product_repo):
    main.dependency_overrides[get_db] = lambda: product_repo.session

    product_repo.create(Product(name="Prod1", price=10.0, available=True))
    product_repo.create(Product(name="Prod2", price=20.0, available=True))

    response = main.test_client().get("/products/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert any(p["name"] == "Prod1" for p in data)
    assert any(p["name"] == "Prod2" for p in data)

def test_create_product(product_repo):
    main.dependency_overrides[get_db] = lambda: product_repo.session

    payload = {
        "name": "New Product",
        "price": 30.0,
        "available": True,
        
    }

    response = main.test_client().post("/products/", json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == payload["name"]
    assert data["price"] == payload["price"]

def test_create_product_invalid(product_repo):
    main.dependency_overrides[get_db] = lambda: product_repo.session

    payload = {
        "name": "",
        "price": -10,
        "available": True,
    }

    response = main.test_client().post("/products/", json=payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST

def test_get_product(product_repo):
    main.dependency_overrides[get_db] = lambda: product_repo.session

    product = product_repo.create(Product(name="GetTest", price=15.0, available=True))
    response = main.test_client().get(f"/products/{product.id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == product.id

def test_get_product_not_found(product_repo):
    main.dependency_overrides[get_db] = lambda: product_repo.session

    response = main.test_client().get("/products/999999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Produto não encontrado"

def test_update_product(product_repo):
    main.dependency_overrides[get_db] = lambda: product_repo.session

    product = product_repo.create(Product(name="OldName", price=10.0, available=True))
    payload = {
        "name": "UpdatedName",
        "price": 12.0,
        "available": False,
    }

    response = main.test_client().put(f"/products/{product.id}", json=payload)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == payload["name"]
    assert data["price"] == payload["price"]
    assert data["available"] == payload["available"]

def test_update_product_not_found(product_repo):
    main.dependency_overrides[get_db] = lambda: product_repo.session

    payload = {
        "name": "NoProduct",
        "price": 10.0,
        "available": True,
    }

    response = main.test_client().put("/products/999999", json=payload)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Produto não encontrado"

def test_delete_product(product_repo):
    main.dependency_overrides[get_db] = lambda: product_repo.session

    product = product_repo.create(Product(name="ToDelete", price=10.0, available=True))
    response = main.test_client().delete(f"/products/{product.id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

def test_delete_product_not_found(product_repo):
    main.dependency_overrides[get_db] = lambda: product_repo.session

    response = main.test_client().delete("/products/999999")
    
    assert response.status_code in (status.HTTP_204_NO_CONTENT, status.HTTP_404_NOT_FOUND)
