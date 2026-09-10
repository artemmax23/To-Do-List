"""
Специализированные CRUD операции для задач (Task).

Содержит функции для создания, чтения, обновления и удаления
задач (Task). Все функции асинхронны и принимают сессию SQLAlchemy 
в качестве первого аргумента.

Зависимости:
        - models: Модели таблиц.
        - schemas: Pydantic-схемы для валидации.
        - base: Общие CRUD операции (дженерики).
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app import models, schemas
from app.crud import base
            
async def get_tasks(
        db: AsyncSession,
        user_id: int,
        skip: int = 0,
        limit: int = 100,
        is_completed: bool | None = None,
        tag_id: int | None = None,
        search: str | None = None,
) -> list[models.Task]:
    """
    Возвращает список задач с фильтрацией, поиском и пагинацией.
    
    Args:
            - db: Асинхронная сессия SQLAlchemy.
            - user_id: ID пользователя
            - skip: Количество записей для пропуска.
            - limit: Максимальное колиество записей.
            - is_completed: Фильтр по статусу выполнения (True/False).
            - tag_id: Фильтр по ID тега.
            - search: Строка для поиска в заголовке и в описании.
            
    Returns:
                 list[models.Task]: Список задач, отсортированный по убыванию ID
    
    Example:
            >>> # Получить невыполненные задачи с поиском
            >>> tasks = await get_tasks(db, is_completed=False, search="купить")
    """
    query = select(models.Task).where(models.Task.user_id == user_id)
    
    # Фильтры
    if is_completed is not None:
        query = query.where(models.Task.is_completed == is_completed) 
    
    if tag_id is not None:
        query = query.where(models.Task.tag_id == tag_id)
        
    if search:
            query = query.where(
                    (models.Task.title.ilike(f"%{search}%")) |
                    (models.Task.description.ilike(f"%{search}%"))
            )    
    
    # Сортировка и пагинация
    query = query.offset(skip).limit(limit).order_by(models.Task.id.desc())
    result = await db.execute(query)            
                                        
    return result.scalars().all()
    
async def create_task(
        db: AsyncSession, 
        user_id: int,
        task: schemas.TaskCreate, 
) -> models.Task:
    """Создаёт новую задачу."""
    return await base.create(db, models.Task, task, user_id)
    
async def get_task(
        db: AsyncSession,
        user_id: int, 
        task_id: int, 
) -> models.Task:
    """Возвращает задачу по ID и None, если не найдена."""
    return await base.get_by_id(db, models.Task, task_id, user_id)
    
async def update_task(
        db: AsyncSession, 
        user_id: int,
        task_id: int, 
        task_update: schemas.TaskUpdate | dict, 
)  -> models.Task | None:
    """Обновляет задачу по ID. Принимает схему и словарь."""
    return await base.update(db, models.Task, task_id, task_update, user_id)
    
async def delete_task(
        db: AsyncSession, 
        user_id: int,
        task_id: int, 
) -> bool:
    """Удаляет задачу по ID. """ 
    return await base.delete(db, models.Task, task_id, user_id)
