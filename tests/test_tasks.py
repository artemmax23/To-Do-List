"""
Модуль содержит тесты для проверки API задач
"""

import pytest
import uuid
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_task(client: AsyncClient, auth_headers):
    """Создание задачи."""
    response = await client.post(
        "/tasks/", 
        json={"title": "Test Task"}, 
        headers=auth_headers
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["is_completed"] is False
    assert "id" in data

@pytest.mark.asyncio
async def test_create_task_with_tag(client: AsyncClient, auth_headers):
    """Создание задачи с тегом."""
    response = await client.post(
        "/tags/", 
        json={"name": "Test Tag"}, 
        headers=auth_headers
    )
    tag_id = response.json()["id"]
    
    response = await client.post(
        "/tasks/", 
        json={
            "title": "Test Task",
            "tag_id": tag_id,
        }, 
        headers=auth_headers
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["tag_id"] == tag_id
    assert data["is_completed"] is False
    assert "id" in data

@pytest.mark.asyncio
async def test_create_task_with_invalid_tag(client: AsyncClient, auth_headers):
    """Создание задачи с неправильным тегом"""
    response = await client.post(
        "/tasks/", 
        json={
            "title": "Test Task",
            "tag_id": 9999,
        }, 
        headers=auth_headers
    )
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_get_empty_tasks(client: AsyncClient, auth_headers):
    """Получение пустого списка задач."""
    response = await client.get(
        "/tasks/",
        headers=auth_headers
    )
    assert response.status_code == 200
    assert response.json() == []

@pytest.mark.asyncio
async def test_filter_task_by_completed(client: AsyncClient, auth_headers):
    """Фильтрация задач по статусу выполнения."""
    response = await client.post(
        "/tasks/", 
        json={"title": "Test Task"}, 
        headers=auth_headers
    )
    assert response.status_code == 201
    
    response = await client.post(
        "/tasks/", 
        json={
            "title": "Test Task1",
            "is_completed": True    
        }, 
        headers=auth_headers
    )
    assert response.status_code == 201
    
    response = await client.get(
        "/tasks/?is_completed=true",
        headers=auth_headers    
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Test Task1"
    
@pytest.mark.asyncio
async def test_search_tasks(client: AsyncClient, auth_headers):
    """Поиск задач по тексту."""
    response = await client.post(
        "/tasks/", 
        json={"title": "Купить хлеб"}, 
        headers=auth_headers
    )
    assert response.status_code == 201
    
    response = await client.post(
        "/tasks/", 
        json={
            "title": "Сделать отчёт",
            "is_completed": True    
        }, 
        headers=auth_headers
    )
    assert response.status_code == 201
    
    response = await client.get(
        "/tasks/?search=хлеб",
        headers=auth_headers    
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert "хлеб" in data[0]["title"]

@pytest.mark.asyncio
async def test_user_cannot_see_another_user_tasks(client: AsyncClient, auth_headers):
    """Пользователь не видит задачу другого пользователя."""            
    response = await client.post(
        "/tasks/", 
        json={"title": "Test task"}, 
        headers=auth_headers
    )
    assert response.status_code == 201
    
    # Создаём второго пользователя и логинимся
    email2 = f"user2_{uuid.uuid4().hex[:6]}@example.com"
    await client.post(
        "/auth/register",
        json={"email": email2, "password": "qwerty123"}
    )
    login2 = await client.post(
        "/auth/login",
        data={"username": email2, "password": "qwerty123"}
    )
    token2 = login2.json()["access_token"]
    headers2 = {"Authorization": f"Bearer {token2}"}

    # Второй пользователь должен видеть пустой список
    response = await client.get("/tasks/", headers=headers2)
    assert response.status_code == 200
    assert response.json() == []
                                    
@pytest.mark.asyncio
async def test_get_task_by_id(client: AsyncClient, auth_headers):
    """Получение задачи по ID."""
    create_resp = await client.post(
        "/tasks/", 
        json={"title": "Task for get"},
        headers=auth_headers
    )
    task_id = create_resp.json()["id"]
    
    response = await client.get(
        f"/tasks/{task_id}",
        headers=auth_headers
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Task for get"
    
@pytest.mark.asyncio
async def test_update_task(client: AsyncClient, auth_headers):
    """Обновление задачи по ID."""
    create_resp = await client.post(
        "/tasks/", 
        json={"title": "Before Update"},
        headers=auth_headers
    )
    task_id = create_resp.json()["id"]
    
    response = await client.patch(
        f"/tasks/{task_id}", 
        json={"title": "After Update"},
        headers=auth_headers
    )
    assert response.status_code == 200
    assert response.json()["title"] == "After Update"
    
@pytest.mark.asyncio
async def test_delete_task(client: AsyncClient, auth_headers):
    """Удаление задачи по ID."""
    create_resp = await client.post(
        "/tasks/", 
        json={"title": "To Delete"},
        headers=auth_headers
    )
    task_id = create_resp.json()["id"]
   
    response = await client.delete(
        f"/tasks/{task_id}",
        headers=auth_headers
    )
    assert response.status_code == 204
   
    get_response = await client.get(
        f"/tasks/{task_id}",
        headers=auth_headers
    )
    assert get_response.status_code == 404
    