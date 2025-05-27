import pytest
from httpx import AsyncClient
from fastapi import status
from app import main
from utils.database import get_db

@pytest.mark.asyncio
async def test_register_user(async_client, async_session):
    main.dependency_overrides[get_db] = lambda: async_session

    payload = {
        "email": "test@example.com",
        "password": "strongpassword"
    }

    response = await async_client.post("/auth/register", json=payload)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["email"] == payload["email"]
    assert "id" in data

@pytest.mark.asyncio
async def test_register_duplicate_user(async_client, async_session):
    main.dependency_overrides[get_db] = lambda: async_session

    payload = {
        "email": "duplicate@example.com",
        "password": "anypass"
    }

    await async_client.post("/auth/register", json=payload)
    response = await async_client.post("/auth/register", json=payload)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Email already registered"

@pytest.mark.asyncio
async def test_login_user(async_client, async_session):
    main.dependency_overrides[get_db] = lambda: async_session

    payload = {
        "email": "login@example.com",
        "password": "loginpass"
    }

    await async_client.post("/auth/register", json=payload)

    login_data = {
        "username": "login@example.com",
        "password": "loginpass"
    }

    response = await async_client.post("/auth/login", data=login_data)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_login_invalid_credentials(async_client, async_session):
    main.dependency_overrides[get_db] = lambda: async_session

    login_data = {
        "username": "nonexistent@example.com",
        "password": "wrongpass"
    }

    response = await async_client.post("/auth/login", data=login_data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Invalid Credentials"
