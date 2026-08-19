"""
CRUD операции для работы с базой данных.

Содержит функции для создания, чтения, обновления и удаления
задач (Task) и тегов (Tag). Все функции асинхронны и принимают
сессию SQLAlchemy в качестве первого аргумента.
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app import models, schemas
 
 # ======================================================
 # Базовые CRUD операции (дженерики)
 # ======================================================
 
async def get_all(db: AsyncSession, model, skip: int = 0, limit: int = 100):
     """
     Возвращает список объектов модели с пагинацией
     
     Args:
         db: Асинхронная сессия SQLAlchemy.
         model: Класс модели SQLAlchemy.
         skip: Количество записей на пропуск.
         limit: Максимальное количество записей.
         
     Returns:
         list: Список объектов модели.
     """
     # Пагинация
     result = await db.execute(
             select(model).offset(skip).limit(limit)
     )
     
     return result.scalars().all()
     
async def get_by_id(db: AsyncSession, model, obj_id: int):
    """
    Возвращает объект модели по его ID.
    
    Args:
        db: Асинхронная сессия SQLAlchemy.
        model: Класс модели SQLAlchemy (например, Task, Tag).
        obj_id: ID объекта.
        
    Returns:
         Объект модели или None, если объект не найден.
         
    Example:
        >>> task = await  get_by_id(db, models.Task, 1)
    """
    result = await db.execute(
        select(model).where(model.id == obj_id)
    )
    
    return result.scalar_one_or_none()
    
async def create(db: AsyncSession, model, obj_data):
    """
    Создаёт новый объект модели в базе данных.
    
    Args:
            db: Асинхронная сессия SQLAlchemy.
            model: Класс модели SQLAlchemy.
            obj_data: Словарь с данными для создания объекта.
            
    Returns:
            Созданный объект модели с заполненными полями (id, created_at и т.д.)
            
    Example:
            >>> task_data = {"title": "Test", "is_completed": False}
            >>> task = await create(db, models.Task, task_data) 
    """
    if isinstance(obj_data, dict):
        db_obj = model(**obj_data)
    else:
        db_obj = model(**obj_data.model_dump())
    
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    
    return db_obj
    
async def update(db: AsyncSession, model, obj_id: int, obj_data):
    """
    Обновляет объект модели по ID.
    
    Args:
            db: Ассинхронная сессия SQLAlchemy.
            model: Класс модели SQLAlchemy.
            obj_id: ID объекта для обновления.
            update_data: Словарь с полями для обновления.
            
    Returns:
            Обновлённый объект или None, если объект не найден.
            
    Example:
            >>> update_data = {"title": "New Title"}
            >>> task = await update(db, models.Task, 1, update_data)
    """
    db_obj = await get_by_id(db, model, obj_id)
    
    if not db_obj:
        return None
    
    update_data = obj_data if isinstance(obj_data, dict) else obj_data.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        if value is not None:
            setattr(db_obj, key, value)
        
    await db.commit()
    await db.refresh(db_obj)
    
    return db_obj
    
async def delete(db: AsyncSession, model, obj_id: int) -> bool:
    """
    Удаляет объект модели по ID.
    
    Args:
            db: Асинхронная сессия SQLAlchemy.
            model: Класс модели SQLAlchemy.
            obj_id: ID объекта для удаления.
            
    Returns:
            bool: True, если объект был удалён, иначе False
    """
    db_obj = await get_by_id(db, model, obj_id)
    
    if not db_obj:
        return False
        
    await db.delete(db_obj)
    await db.commit()
    
    return True

# ======================================================
# Специализированные CRUD операции для задач (Task)
# ======================================================     
            
async def get_tasks(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100,
        is_completed: bool | None = None,
        tag_id: int | None = None,
        search: str | None = None
) -> list[models.Task]:
    """
    Возвращает список задач с фильтрацией, поиском и пагинацией.
    
    Args:
            db: Асинхронная сессия SQLAlchemy.
            skip: Количество записей для пропуска.
            limit: Максимальное колиество записей.
            is_completed: Фильтр по статусу выполнения (True/False).
            tag_id: Фильтр по ID тега.
            search: Строка для поиска в заголовке и в описании.
            
    Returns:
                 list[models.Task]: Список задач, отсортированный по убыванию ID
    
    Example:
            >>> # Получить невыполненные задачи с поиском
            >>> tasks = await get_tasks(db, is_completed=False, search="купить")
    """
    query = select(models.Task)
    
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
    
async def create_task(db: AsyncSession, task: schemas.TaskCreate) -> models.Task:
    """Создаёт новую задачу."""
    return await create(db, models.Task, task)
    
async def get_task(db: AsyncSession, task_id: int) -> models.Task:
    """Возвращает задачу по ID и None."""
    return await get_by_id(db, models.Task, task_id)
    
async def update_task(db: AsyncSession, task_id: int, task_update: schemas.TaskUpdate | dict)  -> models.Task | None:
    """Обновляет задачу по ID. Принимает схему и словарь."""
    return await update(db, models.Task, task_id, task_update)
    
async def delete_task(db: AsyncSession, task_id: int) -> bool:
    """Удаляет задачу по ID. """ 
    return await delete(db, models.Task, task_id)

# ======================================================
# Специализированные CRUD операции для тегов (Tag)
# ====================================================== 
            
async def get_tags(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[models.Tag]:
    """Возвращает список тегов с пагинацией."""
    return await get_all(db, models.Tag, skip, limit)
    
async def get_tag(db: AsyncSession, tag_id: int) -> models.Tag | None:
    """Возвращает тег по ID или None."""
    return await get_by_id(db, models.Tag, tag_id)

async def get_tag_by_name(db: AsyncSession, name: str) -> models.Tag | None:
    """
    Возвращает тег по имени (регистрозависимо)
    
    Args:
            db: Асинхронная сессия SQLAlchemy.
            search: Часть названия тега.
            
    Returns:
            models.Tag | None: Объект тега или None, если не найден. 
    """
    result = await db.execute(
            select(models.Tag)
            .where(models.Tag.name.ilike(name))
    )
    
    return result.scalar_one_or_none()    
            
async def get_tags_by_search(db: AsyncSession, search: str, skip: int = 0, limit: int = 100) -> list[models.Tag]:
    """
    Возвращает список тегов по имени (регистронезависимо)
    
    Args:
            db: Асинхронная сессия SQLAlchemy.
            search: Часть названия тега.
            skip: Количество записей для пропуска.
            limit: Максимальное колиество записей.
            
    Returns:
            list[models.Tag]: Список тегов, содержащих подстроку в названии:
                
    Example:
            >>> tags = await get_tags_by_search(db, "работ", skip=0, limit=10) 
    """
    result = await db.execute(
            select(models.Tag)
            .where(models.Tag.name.ilike(f"%{search}%"))
            .offset(skip)
            .limit(limit)
    )
    
    return result.scalars().all()
    
async def create_tag(db: AsyncSession, tag: schemas.TagCreate) -> models.Tag:
    """Создаёт новый тег."""
    existing_tag = await get_tag_by_name(db, tag.name)
    
    if existing_tag:
        return existing_tag
        
    return await create(db, models.Tag, tag)
    
async def update_tag(db: AsyncSession, tag_id: int, tag_update: schemas.TagUpdate | dict) -> models.Tag | None:
    """Обновляет тег по ID. Принимает схему или словарь"""
    return await update(db, models.Tag, tag_id, tag_update)
    
async def delete_tag(db: AsyncSession, tag_id: int) -> bool:
    """Удаляет тег по ID."""
    return await delete(db, models.Tag, tag_id)