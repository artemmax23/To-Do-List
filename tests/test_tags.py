"""
Модуль содержит тесты для проверки API тегов
"""

import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_tag(client: AsyncClient):
    """Создание тега."""
    response = await client.post("/tags/", json={"name": "Test Tag"})
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Tag"
    assert "id" in data
    
@pytest.mark.asyncio
async def test_get_empty_tags(client: AsyncClient):
    """Получение пустого списка тегов."""
    response = await client.get("/tags/")
    assert response.status_code == 200
    assert response.json() == []
    
@pytest.mark.asyncio
async def test_get_tag_by_id(client: AsyncClient):
    """Получение тега по ID."""
    create_resp = await client.post("/tags/", json={"name": "Tag for get by id"})
    tag_id = create_resp.json()["id"]
    
    response = await client.get(f"/tags/{tag_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Tag for get by id"
    
@pytest.mark.asyncio
async def test_get_tag_by_name(client: AsyncClient):
    """Получение тега по имени (полное совпадение)."""
    create_resp = await client.post("/tags/", json={"name": "Tag for get by name"})
    tag_name = "Tag for get by name"
    
    response = await client.get(f"/tags/name/{tag_name}")
    assert response.status_code == 200
    assert response.json()["name"] == "Tag for get by name"
    
@pytest.mark.asyncio
async def test_get_tags_by_name(client: AsyncClient):
    """Поиск тегов по имени (частичное совпадение)."""
    create_resp = await client.post("/tags/", json={"name": "Tags for get by name"})
    tag_search = "name"
    
    response = await client.get(f"/tags/search/{tag_search}")
    assert response.status_code == 200
    assert response.json()[0]["name"] == "Tags for get by name"
    
@pytest.mark.asyncio
async def test_update_tag(client: AsyncClient):
    """Обновление тега по ID."""
    create_resp = await client.post("/tags/", json={"name": "Before Update"})
    tag_id = create_resp.json()["id"]
    
    response = await client.put(f"/tags/{tag_id}", json={"name": "After Update"})
    assert response.status_code == 200
    assert response.json()["name"] == "After Update"
    
@pytest.mark.asyncio
async def test_delete_tag(client: AsyncClient):
    """Удаление тега по ID."""
    create_resp = await client.post("/tags/", json={"name": "To Delete"})
    tag_id = create_resp.json()["id"]
    
    response = await client.delete(f"/tags/{tag_id}")
    assert response.status_code == 204
    
    get_response = await client.get(f"/tags/{tag_id}")
    assert get_response.status_code == 404
    