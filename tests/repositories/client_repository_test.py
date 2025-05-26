import pytest
from sqlalchemy.exc import IntegrityError
from models.models import Client
from repositories.client_repository import ClientRepository

@pytest.fixture
def client_repo(db):
    return ClientRepository(session=db)

def test_client_create(client_repo):
    client = Client(name="Test Client", email="test@client.com", cpf="123.456.789-00")
    created = client_repo.create(client)
    assert created.id is not None
    assert created.name == "Test Client"

def test_client_create_duplicate_email(client_repo):
    client1 = Client(name="A", email="dup@test.com", cpf="111.111.111-11")
    client_repo.create(client1)
    client_repo.session.commit()

    client2 = Client(name="B", email="dup@test.com", cpf="222.222.222-22")

    with pytest.raises(IntegrityError):
        client_repo.create(client2)
    client_repo.session.rollback()

def test_client_create_duplicate_cpf(client_repo):
    client1 = Client(name="A", email="unique@test.com", cpf="333.333.333-33")
    client_repo.create(client1)
    client_repo.session.commit()

    client2 = Client(name="B", email="other@test.com", cpf="333.333.333-33")
    with pytest.raises(IntegrityError):
        client_repo.create(client2)
    client_repo.session.rollback()

def test_client_get(client_repo):
    client = Client(name="Cliente Get", email="get@test.com", cpf="444.444.444-44")
    client_repo.create(client)
    client_repo.session.commit()

    found = client_repo.get(client.id)
    assert found is not None
    assert found.email == "get@test.com"

def test_client_get_nonexistent(client_repo):

    found = client_repo.get(999999)
    assert found is None

def test_client_update(client_repo):
    client = Client(name="Cliente Upd", email="upd@test.com", cpf="555.555.555-55")
    created = client_repo.create(client)
    client_repo.session.commit()

    updated = client_repo.update(created, {"name": "Client Updated"})
    assert updated.name == "Client Updated"
    assert updated.id == created.id

def test_client_update_by_id(client_repo):
    client = Client(name="Cliente UpdId", email="upid@test.com", cpf="666.666.666-66")
    created = client_repo.create(client)
    client_repo.session.commit()

    updated = client_repo.update_by_id(created.id, {"email": "newemail@test.com"})
    assert updated.email == "newemail@test.com"
    assert updated.id == created.id

def test_client_update_by_id_nonexistent(client_repo):
    with pytest.raises(ValueError):
        client_repo.update_by_id(999999, {"name": "Nobody"})

def test_client_delete(client_repo):
    client = Client(name="Client Del", email="del@test.com", cpf="777.777.777-77")
    created = client_repo.create(client)
    client_repo.session.commit()

    client_repo.delete(created)
    deleted = client_repo.get(created.id)
    assert deleted is None
