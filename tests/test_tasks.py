"""
Модуль содержит тесты для проверки API задач
"""

import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_task(client: AsyncClient):
    """Создание задачи."""
    response = await client.post("/tasks/", json={"title": "Test Task"})
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["is_completed"] is False
    assert "id" in data
    
@pytest.mark.asyncio
async def test_get_empty_tasks(client: AsyncClient):
    """Получение пустого списка задач."""
    response = await client.get("/tasks/")
    assert response.status_code == 200
    assert response.json() == []
    
@pytest.mark.asyncio
async def test_get_task_by_id(client: AsyncClient):
    """Получение задачи по ID."""
    create_resp = await client.post("/tasks/", json={"title": "Task for get"})
    task_id = create_resp.json()["id"]
    
    response = await client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Task for get"
    
@pytest.mark.asyncio
async def test_update_task(client: AsyncClient):
    """Обновление задачи по ID."""
    create_resp = await client.post("/tasks/", json={"title": "Before Update"})
    task_id = create_resp.json()["id"]
    
    response = await client.patch(f"/tasks/{task_id}", json={"title": "After Update"})
    assert response.status_code == 200
    assert response.json()["title"] == "After Update"
    
@pytest.mark.asyncio
async def test_delete_task(client: AsyncClient):
    """Удаление задачи по ID."""
    create_resp = await client.post("/tasks/", json={"title": "To Delete"})
    task_id = create_resp.json()["id"]
   
    response = await client.delete(f"/tasks/{task_id}")
    assert response.status_code == 204
   
    get_response = await client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 404
    