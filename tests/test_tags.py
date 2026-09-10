"""
Модуль содержит тесты для проверки API тегов
"""

import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_tag(client: AsyncClient, auth_headers):
    """Создание тега."""                        
    response = await client.post(
            "/tags/", 
            json={"name": "Test Tag"}, 
            headers=auth_headers
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Tag"
    assert "id" in data
    
@pytest.mark.asyncio
async def test_get_empty_tags(client: AsyncClient, auth_headers):
    """Получение пустого списка тегов."""
    response = await client.get(
            "/tags/", 
            headers=auth_headers
            )
    assert response.status_code == 200
    assert response.json() == []
    
@pytest.mark.asyncio
async def test_get_tag_by_id(client: AsyncClient, auth_headers):
    """Получение тега по ID."""
    create_resp = await client.post(
            "/tags/", 
            json={"name": "Tag for get by id"},
            headers=auth_headers
    )
    tag_id = create_resp.json()["id"]
    
    response = await client.get(
            f"/tags/{tag_id}",
            headers=auth_headers
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Tag for get by id"
    
@pytest.mark.asyncio
async def test_get_tag_by_name(client: AsyncClient, auth_headers):
    """Получение тега по имени (полное совпадение)."""
    create_resp = await client.post(
            "/tags/", 
            json={"name": "Tag for get by name"},
            headers=auth_headers
    )
    tag_name = "Tag for get by name"
    
    response = await client.get(
            f"/tags/name/{tag_name}",
            headers=auth_headers
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Tag for get by name"
    
@pytest.mark.asyncio
async def test_get_tags_by_name(client: AsyncClient, auth_headers):
    """Поиск тегов по имени (частичное совпадение)."""
    create_resp = await client.post(
            "/tags/", 
            json={"name": "Tags for get by name"},
            headers=auth_headers
    )
    tag_search = "name"
    
    response = await client.get(
            f"/tags/search/{tag_search}",
            headers=auth_headers
    )
    assert response.status_code == 200
    assert response.json()[0]["name"] == "Tags for get by name"
    
@pytest.mark.asyncio
async def test_update_tag(client: AsyncClient, auth_headers):
    """Обновление тега по ID."""
    create_resp = await client.post(
            "/tags/", 
            json={"name": "Before Update"},
            headers=auth_headers
    )
    tag_id = create_resp.json()["id"]
    
    response = await client.put(
            f"/tags/{tag_id}", 
            json={"name": "After Update"},
            headers=auth_headers
    )
    assert response.status_code == 200
    assert response.json()["name"] == "After Update"
    
@pytest.mark.asyncio
async def test_delete_tag(client: AsyncClient, auth_headers):
    """Удаление тега по ID."""
    create_resp = await client.post(
            "/tags/", 
            json={"name": "To Delete"},
            headers=auth_headers
    )
    tag_id = create_resp.json()["id"]
    
    response = await client.delete(
            f"/tags/{tag_id}",
            headers=auth_headers
    )
    assert response.status_code == 204
    
    get_response = await client.get(
            f"/tags/{tag_id}",
            headers=auth_headers
    )
    assert get_response.status_code == 404
    
@pytest.mark.asyncio
async def test_create_duplicate_tag(client: AsyncClient, auth_headers):
    """Создание тега с дублирующимся именем."""
    # Создаём первый тег
    await client.post(
        "/tags/",
        json={"name": "Duplicate"},
        headers=auth_headers
    )

    # Пытаемся создать второй с таким же именем
    response = await client.post(
        "/tags/",
        json={"name": "Duplicate"},
        headers=auth_headers
    )
    assert response.status_code == 201  # Или 400, если запрещено дублирование
    assert response.json()["name"] == "Duplicate"