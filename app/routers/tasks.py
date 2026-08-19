"""
Маршруты (роутеры) для работы с задачами

Предоставляет полный набор эндпоинтов для управления задачами:
- Создание (POST /tasks/)
- Получения списка с пагинацией и фильтрацией (GET /tasks/)
- Получение по ID (GET /tasks/{task_id})
- Полное обновление (PUT /tasks/{task_id})
- Частичное обновление (PATCH /tasks/{task_id})
- Удаление (DELETE /tasks/{task_id})

Все эдпоинты используют асинхронные сессии SQLAlchemy и валидацию через Pydantic
Автоматическая документация доступна в Swagger (/docs) и ReDoc (/redoc)

Зависимости:
        - get_db: внедряет асинхронную сессию базы данных.
        - crud: функции для работы с базой данных.
        - schemas: Pydantic-схемы для валидации запросов и ответов.
        
Пример:
        >>> # Создать задачу
        >>> POST /tasks/
        >>> {
        ...            "title": "Купить продукты",
        ...            "description": "Молоко, хлеб, яйца",
        ...            "tag_id": 1
        ...    }
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from app import crud, schemas, models
from app.database import get_db

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get(
        "/", 
        response_model=list[schemas.TaskResponse],
        summary="Получить список задач"
)
async def read_tasks(
        db: AsyncSession = Depends(get_db),
        page: int = Query(1, ge=1, description="Номер страницы"),
        limit: int = Query(10, ge=1, le=100, description="Количество задач на странице"),
        is_completed: bool | None = Query(None, description="Фильтр по статусу выполнения"),
        tag_id : int | None = Query(None, description="Фильтр по ID тега"),
        search: str | None = Query(None, description="Поиск по названию или описанию") 
):
    """
    Получить список задач с пагинацией и фильтрацией.
    
    Args:
            - db: Асинхронная сессия SQLAlchemy.
            - page: Номер страницы (по умолчанию 1).
            - limit: Количество на странице (по умолчанию 10).
            - is_completed: Фильтр по статусу (True/False).
            - tag_id: Фильтр по тегу.
            - search:  Поиск по заголовку или описанию.
    
    Returns:
            list[schemas.TaskResponse]: Список задач, соответствующих фильтрам.  
            
    Raises:
            HTTPException: 500, при внутренней ошибке сервера.   
                            
    Example:
            ```http
            GET /tasks?page=2&limit=5&is_completed=false&search=купить
            ```
    
    Response:
            ```json
           [
                {
                        "id": 1,
                        "title": "Купить продукты",
                        "description": "Молоко, хлеб, яйца",
                        "is_completed": false,
                        "created_at": "2026-08-19T10:00:00+00:00",
                        "updated_at": null,
                        "tag_id": 1
                }
            ]
            ```
    """
    offset = (page - 1) * limit
    
    return await crud.get_tasks(
                                db, 
                                skip=offset, 
                                limit=limit,
                                is_completed=is_completed,
                                tag_id=tag_id,
                                search=search
    )

@router.post(
        "/", 
        response_model=schemas.TaskResponse,
        status_code=status.HTTP_201_CREATED,
        summary="Создать новую задачу"
)    
async def create_task(
        task: schemas.TaskCreate, 
        db: AsyncSession = Depends(get_db)
):
    """
    Создание задачи.
    
    Args:
            - task: Pydantic-схема с данными для создания задачи (title, description, is_completed, tag_id).
            - db: Асинхронная сессия SQLAlchemy.
    
    Returns:
            schemas.TaskResponse: Созданная задача с полями id, created_at и updated_at.        
     
     Raises:
            HTTPException: 500, при внутренней ошибке сервера.
            HTTPException: 404, если переданный tag_id не существует в базе данных.                   
                                                                          
    Example:
            ```http
            POST /tasks/
            Content-Type: application/json
            
            {
                "title": "Купить продукты",
                "description": "Молоко, хлеб, яйца",
                "tag_id": 1
             }
            ```
    Response:
            ```json
            {
                    "id": 1,
                    "title": "Купить продукты",
                    "description": "Молоко, хлеб, яйца",
                    "is_completed": false,
                    "created_at": "2026-08-19T10:00:00+00:00",
                    "updated_at": null,
                    "tag_id": 1
            }
            ```
    """
    
    # Проверка существования тега
    if task.tag_id:
        tag = await crud.get_tag(db, task.tag_id)
        if not tag:
            raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Tag with id {task.tag_id} not found"
            )
            
    return await crud.create_task(db, task)
    
@router.get(
        "/{task_id}",
        response_model=schemas.TaskResponse,
        summary="Получить задачу по ID"
)
async def get_task(
        task_id: int,
        db: AsyncSession = Depends(get_db)
):
    """
    Получение задачи по ID.
    
    Args:
            - task_id: ID задачи.
            - db: Асинхронная сессия SQLAlchemy.
    
    Returns:
            schemas.TaskResponse: Задача с соответствующим ID.        
     
     Raises:
            HTTPException: 500, при внутренней ошибке сервера.
            HTTPException: 404, если задачи с таким ID не существует в базе данных.                   
                                                                          
    Example:
            ```http
            GET /tasks/1
            ```
    Response:
            ```json
            {
                    "id": 1,
                    "title": "Купить продукты",
                    "description": "Молоко, хлеб, яйца",
                    "is_completed": false,
                    "created_at": "2026-08-19T10:00:00+00:00",
                    "updated_at": null,
                    "tag_id": 1
            }
            ```
    """
    task = await crud.get_task(db, task_id)
   
    # Проверка существования задачи 
    if not task:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task with id {task_id} not found"
        )
        
    return task
    
@router.put(
    "/{task_id}",
    response_model=schemas.TaskResponse,
    summary="Полное обновление задачи"    
)
async def update_task(
        task_id: int,
        task_data: schemas.TaskUpdate,
        db: AsyncSession = Depends(get_db)
):
    """
    Полное обновление задачи.
    
    Args:
            - task_id: ID задачи для изменения.
            - task_data: Pydantic-схема с данными для полного обновления задачи (title, description, is_completed, tag_id).
            - db: Асинхронная сессия SQLAlchemy.
    
    Returns:
            schemas.TaskResponse: Обновленная задача с полями id, created_at и updated_at.        
     
     Raises:
            HTTPException: 500, при внутренней ошибке сервера.
            HTTPException: 404, если задача с указанным ID не существует в базе данных.
            HTTPException: 404, если переданный tag_id не существует в базе данных.                   
                                                                          
    Example:
            ```http
            PUT /tasks/1
            Content-Type: application/json
            
            {
                "title": "Купить продукты и средства гигиены",
                "description": "Молоко, хлеб, яйца, шампунь",
                "is_completed": true,
                "tag_id": 2
             }
            ```
    Response:
            ```json
            {
                    "id": 1,
                    "title": "Купить продукты и средства гигиены",
                    "description": "Молоко, хлеб, яйца, шампунь",
                    "is_completed": true,
                    "created_at": "2026-08-19T10:00:00+00:00",
                    "updated_at": "2026-08-19T11:00:00+00:00",
                    "tag_id": 2
            }
            ```
    """
    existing_task = await crud.get_task(db, task_id)
   
   # Проверка существования задачи
    if not existing_task:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task with id {task_id} not found"
        )
    
    # Проверка существования тега (если передан)
    if task_data.tag_id:
        tag = await crud.get_tag(db, task_data.tag_id)
        
        if not tag:
            raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Tag with id {task_data.tag_id} not found"
            )    
                
    return await crud.update_task(db, task_id, task_data)
    
@router.patch(
        "/{task_id}",
        response_model=schemas.TaskResponse,
        summary="Частично обновить задачу"
)
async def patch_task(
        task_id: int,
        task_data: schemas.TaskPatch,
        db: AsyncSession = Depends(get_db)
) :
    """
    Частичное обновление задачи.
    
    Args:
            - task_id: ID задачи для изменения.
            - task_data: Pydantic-схема с данными для частичного обновления задачи 
                                 (title, description, is_completed, tag_id). Все поля опциональны.
            - db: Асинхронная сессия SQLAlchemy.
    
    Returns:
            schemas.TaskResponse: Обновленная задача с полями id, created_at и updated_at.        
     
     Raises:
            HTTPException: 500, при внутренней ошибке сервера.
            HTTPException: 404, если задача с указанным ID не существует в базе данных.
            HTTPException: 404, если переданный tag_id не существует в базе данных.                   
                                                                          
    Example:
            ```http
            PATCH /tasks/1
            Content-Type: application/json
            
            {
                "is_completed": true,
             }
            ```
    Response:
            ```json
            {
                    "id": 1,
                    "title": "Купить продукты",
                    "description": "Молоко, хлеб, яйца",
                    "is_completed": true,
                    "created_at": "2026-08-19T10:00:00+00:00",
                    "updated_at": "2026-08-19T11:00:00+00:00",
                    "tag_id": 1
            }
            ```
    """
    existing_task = await crud.get_task(db, task_id)
    
    # Проверка существования задачи
    if not existing_task:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task with id {task_id} not found"
        )
    
    # Проверка существования тега (если передан)
    if task_data.tag_id:
        tag = await crud.get_tag(db, task_data.tag_id)
        
        if not tag:
            raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Tag with id {task_data.tag_id} not found"
            )
            
    return await crud.update_task(db, task_id, task_data.model_dump(exclude_unset=True))
    
@router.delete(
        "/{task_id}",
        status_code=status.HTTP_204_NO_CONTENT,
        summary="Удалить задачу"
)
async def delete_task(
        task_id: int,
        db: AsyncSession = Depends(get_db)
):
    """
    Удаление задачи.
    
    Args:
            - task_id: ID задачи для изменения.
            - db: Асинхронная сессия SQLAlchemy.       
     
     Returns:
             None: При успешном выполнении возвращается статус 204 No Content.
     
     Raises:
            HTTPException: 500, при внутренней ошибке сервера.
            HTTPException: 404, если задача с указанным ID не существует в базе данных.     
                                                                          
    Example:
            ```http
            DELETE /tasks/1
            ```
    Response:
            ```http
            HTTP/1.1 204 No Content
            ```
    """
    deleted = await crud.delete_task(db, task_id)
    
    # Проверка удаления задачи
    if not deleted:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task with id {task_id} not found"
        )
        
    return None