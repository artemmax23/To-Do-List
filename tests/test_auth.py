"""
Модуль содержит тесты для проверки API авторизации.
"""

import pytest, uuid
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_register_user(client: AsyncClient):
    """Регистрация пользователя."""
    response = await client.post(
            "/auth/register", 
            json={
                    "email": "test@example.com",
                    "password": "qwerty123"
            }
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["is_active"] is False
    assert "id" in data
    
@pytest.mark.asyncio
async def test_correct_login(client: AsyncClient, create_test_user):
    """Авторизация пользователя с правильными данными."""
    user = create_test_user
    
    response = await client.post(
            "/auth/login", 
            data={
                    "username": user["email"],
                    "password": user["password"]
            }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    
@pytest.mark.asyncio
async def test_incorrect_password_login(client: AsyncClient, create_test_user):
    """Некорректный пароль пользователя."""
    user = create_test_user
    
    response = await client.post(
            "/auth/login", 
            data={
                    "username": user["email"],
                    "password": "=1l,nnxkxks"
            }
    )
    
    assert response.status_code == 401
    
@pytest.mark.asyncio
async def test_incorrect_email_login(client: AsyncClient, create_test_user):
    """Некорректный email пользователя."""
    user = create_test_user
    
    response = await client.post(
            "/auth/login", 
            data={
                    "username": f"user_{uuid.uuid4().hex[:6]}@example.com",
                    "password": user["password"]
            }
    )
    
    assert response.status_code == 401
    
@pytest.mark.asyncio
async def test_duplicate_email_register(client: AsyncClient, create_test_user):
    """Регистрация с уже существующим email."""
    user = create_test_user
    
    response = await client.post(
            "/auth/register", 
            json={
                    "email": user["email"],
                    "password": user["password"]
            }
    )
    
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

@pytest.mark.asyncio
async def test_protected_endpoint_without_token(client: AsyncClient):
    """Доступ к защищённому эндпоинту без токена."""
    response = await client.get("/tasks/")
    
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"
    
@pytest.mark.asyncio
async def test_protected_endpoint_with_invalid_token(client: AsyncClient):
    """Доступ к защищённому эндпоинту с невалидным токеном."""
    headers = {"Authorization": "Bearer invalid_token"}
    response = await client.get("/tasks/", headers=headers)
    
    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials"