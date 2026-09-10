"""
Маршруты (роутеры) для работы с тегами

Предоставляет полный набор эндпоинтов для управления тегами
- Создание (POST /tags/)
- Получения списка с пагинацией (GET /tags/)
- Получение по ID (GET /tags/{tag_id})
- Получение по имени (GET /tags/name/{tag_name})
- Поиск по имени (GET /tags/search/{tag_search})
- Полное обновление (PUT /tags/{tag_id})
- Удаление (DELETE /tags/{tag_id})

Все эндпоинты используют асинхронные сессии SQLAlchemy и валидацию через Pydantic
Автоматическая документация доступна в Swagger (/docs) и ReDoc (/redoc)

Зависимости:
        - get_db: внедряет асинхронную сессию базы данных.
        - crud: функции для работы с базой данных.
        - schemas: Pydantic-схемы для валидации запросов и ответов.
        - get_current_user: Получение текущего пользователя.
        
Пример:
        >>> # Создать тег
        >>> POST /tags/
        >>> {
        ...           "name": "Продукты",
        ...    }
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from app import crud, schemas, models
from app.database import get_db
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/tags", tags=["tags"])

@router.get(
        "/",
        response_model=list[schemas.TagResponse],
        summary="Получить список всех тегов"
)
async def read_tags(
        db: AsyncSession = Depends(get_db),
        user: models.User = Depends(get_current_user),
        page: int = Query(1, ge=1, description="Номер страницы"),
        limit: int = Query(10, ge=1, le=100, description="Количество тегов на странице"),
):
    """
    Получить список тегов с пагинацией.
    
    Args:
            - db: Асинхронная сессия SQLAlchemy.
            - user: Текущий пользователь.
            - page: Номер страницы (по умолчанию 1).
            - limit: Количество на странице (по умолчанию 10).
    
    Returns:
            list[schemas.TagResponse]: Список тегов.  
            
    Raises:
            HTTPException: 500, при внутренней ошибке сервера.   
                            
    Example:
            ```http
            GET /tags?page=1&limit=5
            ```
            
    Response:
            ```json
            [
                {
                        "id": 1,
                        "name": "Продукты"
                }
            ]
            ```
    """
    
    offset = (page - 1) * limit
  
    return await crud.get_tags(db, user.id, offset, limit)
    
@router.get(
        "/{tag_id}",
        response_model=schemas.TagResponse,
        summary="Получение тега по id"
)  
async def get_tag(
        tag_id: int,
        db: AsyncSession = Depends(get_db),
        user: models.User = Depends(get_current_user)
):
    """
    Получение тега по ID.
    
    Args:
            - tag_id: ID тега.
            - db: Асинхронная сессия SQLAlchemy.
            - user: Текущий пользователь.
    
    Returns:
            schemas.TagResponse: Тег с соответствующим ID.        
     
     Raises:
            HTTPException: 500, при внутренней ошибке сервера.
            HTTPException: 404, если тега с указанным ID не существует в базе данных.                   
                                                                          
    Example:
            ```http
            GET /tags/1
            ```
    Response:
            ```json
            {
                    "id": 1,
                    "name": "Продукты"
            }
            ```
    """
    
    tag = await crud.get_tag(db, user.id, tag_id)
   
    # Проверка существования тега
    if not tag:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tag with id {tag_id} not found"
        )
    
    return tag
    
@router.get(
        "/search/{tag_search}",
        response_model=list[schemas.TagResponse],
        summary="Поиск тегов по имени"
)
async def get_tags_by_search(
        tag_search: str,
        db: AsyncSession = Depends(get_db),
        user: models.User = Depends(get_current_user),
        page: int = Query(1, ge=1, description="Номер страницы"),
        limit: int = Query(10, ge=1, le=100, description="Количество тегов на странице"),
):
    """
    Поиск тегов по имени.
    
    Args:
            - tag_search: Часть имени тега.
            - db: Асинхронная сессия SQLAlchemy.
            - user: Текущий пользователь.
            - page: Номер страницы (по умолчанию 1).
            - limit: Количество на странице (по умолчанию 10).
    
    Returns:
            list[schemas.TagResponse]: Список тегов, содержащих в названии tag_search.        
     
     Raises:
            HTTPException: 500, при внутренней ошибке сервера.                   
                                                                          
    Example:
            ```http
            GET /tags/search/Про
            ```
    Response:
            ```json
            [
                {
                        "id": 1,
                        "name": "Продукты"
                }
            ]
            ```
    """
    offset = (page - 1) * limit
    
    return await crud.get_tags_by_search(db, user.id, tag_search, offset, limit)
    
@router.get(
        "/name/{tag_name}",
        response_model=schemas.TagResponse,
        summary="Поиск тегов по названию"
)
async def get_tag_by_name(
        tag_name: str,
        db: AsyncSession=Depends(get_db),
        user: models.User = Depends(get_current_user)
):
    """
    Получить тег по имени (полное совпадение).
    
    Args:
            - tag_name: Имя тега.
            - db: Асинхронная сессия SQLAlchemy.
            - user: Текущий пользователь.
    
    Returns:
            schemas.TagResponse: Тегов с  именем.        
     
     Raises:
            HTTPException: 500, при внутренней ошибке сервера.
            HTTPException: 404, если тега с указанным именем не существует в базе данных.                   
                                                                          
    Example:
            ```http
            GET /tags/name/Продукты
            ```
    Response:
            ```json
            {
                    "id": 1,
                    "name": "Продукты"
            }
            ```
    """
    tag = await crud.get_tag_by_name(db, user.id, tag_name)
    
    # Проверка существования тега
    if not tag:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tag with name '{tag_name}'' not found"
        )
    
    return tag

@router.post(
        "/",
        response_model=schemas.TagResponse,
        status_code=status.HTTP_201_CREATED,
        summary="Создание тега"
)
async def create_tag(
        tag: schemas.TagCreate,
        db: AsyncSession=Depends(get_db),
        user: models.User = Depends(get_current_user)
):
    """
    Создание тега.
    
    Args:
            - tag: Pydantic-схема с данными для создания тега (name).
            - db: Асинхронная сессия SQLAlchemy.
            - user: Текущий пользователь.
    
    Returns:
            schemas.TagResponse: Созданный тег с полем id.        
     
     Raises:
            HTTPException: 500, при внутренней ошибке сервера.                   
                                                                          
    Example:
            ```http
            POST /tags/
            Content-Type: application/json
            
            {
                "name": "Продукты"
            }
            ```
    Response:
            ```json
            {
                    "id": 1,
                    "name": "Продукты"
            }
            ```
    """
    return await crud.create_tag(db, user.id, tag)
    
@router.put(
        "/{tag_id}",
        response_model=schemas.TagResponse,
        summary="Обновление тега"
)
async def update_tag(
        tag_id: int,
        tag_data: schemas.TagUpdate,
        db: AsyncSession = Depends(get_db),
        user: models.User = Depends(get_current_user)
):
    """
    Обновление тега.
    
    Args:
            - tag_id: ID тега для изменения.
            - tag_data: Pydantic-схема с данными для обновления тега (name).
            - db: Асинхронная сессия SQLAlchemy.
            - user: Текущий пользователь.
    
    Returns:
            schemas.TagResponse: Обновленный тег с полем id.        
     
     Raises:
            HTTPException: 500, при внутренней ошибке сервера.
            HTTPException: 404, если задача с указанным ID не существует в базе данных.                  
                                                                          
    Example:
            ```http
            PUT /tags/1
            Content-Type: application/json
            
            {
                "name": "Продукты 1"
             }
            ```
    Response:
            ```json
            {
                    "id": 1,
                    "name": "Продукты 1"
            }
            ```
    """
    
    existing_tag = await crud.update_tag(db, user.id, tag_id, tag_data)
    
    # Проверка тега на существование
    if not existing_tag:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tag with id {tag_id} not found"
        )
        
    return existing_tag
    
@router.delete(
        "/{tag_id}",
        status_code=status.HTTP_204_NO_CONTENT,
        summary="Удалить тег"
)
async def delete_tag(
        tag_id: int,
        db: AsyncSession=Depends(get_db),
        user: models.User = Depends(get_current_user)
):
    """
    Удаление тега.
    
    Args:
            - tag_id: ID тега для изменения.
            - db: Асинхронная сессия SQLAlchemy.  
            - user: Текущий пользователь.     
     
     Returns:
             None: При успешном выполнении возвращается статус 204 No Content.
     
     Raises:
            HTTPException: 500, при внутренней ошибке сервера.
            HTTPException: 404, если тег с указанным ID не существует в базе данных.     
                                                                          
    Example:
            ```http
            DELETE /tags/1
            ```
    Response:
            ```http
            HTTP/1.1 204 No Content
            ```
    """
    deleted = await crud.delete_tag(db, user.id, tag_id) 
    
    if not deleted:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tag with id {tag_id} not found"
        )
        
    return None