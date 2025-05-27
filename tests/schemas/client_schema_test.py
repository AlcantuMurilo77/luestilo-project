import pytest
from pydantic import ValidationError
from app.network.schemas.client import ClientCreate

def test_valid_client_creation():
    client = ClientCreate(name="João",
                          email="joao@email.com",
                          cpf="12312312312")
    assert client.name == "João"

def test_invalid_client_name():
    with pytest.raises(ValidationError):
        ClientCreate(name="Jo", email="joao@email.com", cpf="12312312312")

def test_invalid_client_email():
    with pytest.raises(ValidationError):
        ClientCreate(name="João", email="invalid", cpf="12312312312")

def test_invalid_client_cpf():
    with pytest.raises(ValidationError):
        ClientCreate(name="João", email="joao@email.com", cpf="123")
