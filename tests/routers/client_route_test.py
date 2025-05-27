import pytest
from fastapi import status
from main import app
from utils.database import override_get_db
from models.models import User
from core.security import create_access_token

@pytest.fixture
def client_repo(session):
    from repositories.client_repository import ClientRepository
    return ClientRepository(session)

@pytest.mark.parametrize("payload", [
    {"name": "João Teste", "email": "joao@example.com", "cpf": "12345678901"},
])
def test_create_client(client_repo, payload):
    app.dependency_overrides[override_get_db] = lambda: client_repo.session

    response = app.test_client().post("/clients/", json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["email"] == payload["email"]
    assert data["cpf"] == payload["cpf"]

def test_create_client_duplicate_email(client_repo):
    app.dependency_overrides[override_get_db] = lambda: client_repo.session

    p1 = {"name": "Cliente1", "email": "dup@example.com", "cpf": "11111111111"}
    p2 = {"name": "Cliente2", "email": "dup@example.com", "cpf": "22222222222"}

    client_repo.create(client_repo.model(**p1))
    response = app.test_client().post("/clients/", json=p2)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Email já cadastrado"

def test_create_client_duplicate_cpf(client_repo):
    app.dependency_overrides[override_get_db] = lambda: client_repo.session

    p1 = {"name": "ClienteA", "email": "a@example.com", "cpf": "99999999999"}
    p2 = {"name": "ClienteB", "email": "b@example.com", "cpf": "99999999999"}

    client_repo.create(client_repo.model(**p1))
    response = app.test_client().post("/clients/", json=p2)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "CPF já cadastrado"

def test_list_clients(client_repo):
    app.dependency_overrides[override_get_db] = lambda: client_repo.session

    client_repo.create(client_repo.model(name="Test1", email="test1@example.com", cpf="11111111111"))
    client_repo.create(client_repo.model(name="Test2", email="test2@example.com", cpf="22222222222"))

    response = app.test_client().get("/clients/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) >= 2

def test_get_client(client_repo):
    app.dependency_overrides[override_get_db] = lambda: client_repo.session

    c = client_repo.create(client_repo.model(name="GetTest", email="gettest@example.com", cpf="33333333333"))
    response = app.test_client().get(f"/clients/{c.id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == c.id

def test_get_client_not_found(client_repo):
    app.dependency_overrides[override_get_db] = lambda: client_repo.session

    response = app.test_client().get("/clients/999999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Cliente não encontrado"

def test_update_client(client_repo):
    app.dependency_overrides[override_get_db] = lambda: client_repo.session

    c = client_repo.create(client_repo.model(name="UpdateTest", email="updatetest@example.com", cpf="44444444444"))
    payload = {"name": "Updated Name", "email": "updatetest@example.com", "cpf": "44444444444"}

    response = app.test_client().put(f"/clients/{c.id}", json=payload)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == "Updated Name"

def test_update_client_not_found(client_repo):
    app.dependency_overrides[override_get_db] = lambda: client_repo.session

    payload = {"name": "NoUser", "email": "nouser@example.com", "cpf": "55555555555"}
    response = app.test_client().put("/clients/999999", json=payload)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Cliente não encontrado"

def test_delete_client(client_repo):
    app.dependency_overrides[override_get_db] = lambda: client_repo.session

    admin_user = User(email="admin@test.com", hashed_password="fake", is_admin=True)
    client_repo.session.add(admin_user)
    client_repo.session.commit()

    from core.security import create_access_token
    token = create_access_token({"sub": admin_user.email, "is_admin": True})


    client = client_repo.create(client_repo.model(name="DeleteTest", email="deletetest@example.com", cpf="66666666666"))

    headers = {"Authorization": f"Bearer {token}"}
    response = app.test_client().delete(f"/clients/{client.id}", headers=headers)
    assert response.status_code == status.HTTP_204_NO_CONTENT

def test_delete_client_not_found(client_repo):
    app.dependency_overrides[override_get_db] = lambda: client_repo.session

    admin_user = User(email="admin2@test.com", hashed_password="fake", is_admin=True)
    client_repo.session.add(admin_user)
    client_repo.session.commit()

    from core.security import create_access_token
    token = create_access_token({"sub": admin_user.email, "is_admin": True})

    headers = {"Authorization": f"Bearer {token}"}
    response = app.test_client().delete("/clients/999999", headers=headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Cliente não encontrado"
