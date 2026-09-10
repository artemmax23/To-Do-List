"""
Общие CRUD операции (дженерики) для работы с базой данных.

Содержит общие функции для создания, чтения, обновления и удаления
объектов. Все функции асинхронны и принимают сессию SQLAlchemy в качестве 
первого аргумента.
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
 
async def get_all(
        db: AsyncSession, 
        model, 
        skip: int = 0, 
        limit: int = 100, 
        user_id: int | None = None
):
     """
     Возвращает список объектов модели с пагинацией
     
     Args:
         db: Асинхронная сессия SQLAlchemy.
         model: Класс модели SQLAlchemy.
         skip: Количество записей на пропуск.
         limit: Максимальное количество записей.
         user_id: ID пользователя.
         
     Returns:
         list: Список объектов модели.
     """
     # Пагинация
     query = select(model)
     
     if user_id is not None and hasattr(model, "user_id"):
         query = query.where(model.user_id == user_id) 
     
     query = query.offset(skip).limit(limit)
     result = await db.execute(query)
     
     return result.scalars().all()
     
async def get_by_id(
        db: AsyncSession, 
        model, 
        obj_id: int, 
        user_id: int | None = None
):
    """
    Возвращает объект модели по его ID.
    
    Args:
        db: Асинхронная сессия SQLAlchemy.
        model: Класс модели SQLAlchemy (например, Task, Tag).
        obj_id: ID объекта.
        user_id: ID пользователя.
        
    Returns:
         Объект модели или None, если объект не найден.
         
    Example:
        >>> task = await  get_by_id(db, models.Task, 1)
    """
    query = select(model)
    
    if user_id is not None and hasattr(model, "user_id"):
         query = query.where(model.user_id == user_id)
    
    query = query.where(model.id == obj_id)
    result = await db.execute(query)
    
    return result.scalar_one_or_none()
    
async def create(
        db: AsyncSession, 
        model, 
        obj_data,
        user_id: int | None = None
):
    """
    Создаёт новый объект модели в базе данных.
    
    Args:
            db: Асинхронная сессия SQLAlchemy.
            model: Класс модели SQLAlchemy.
            obj_data: Словарь с данными для создания объекта.
            user_id: ID пользователя.
            
    Returns:
            Созданный объект модели с заполненными полями (id, created_at и т.д.)
            
    Example:
            >>> task_data = {"title": "Test", "is_completed": False}
            >>> task = await create(db, models.Task, task_data) 
    """    
    if isinstance(obj_data, dict):
        data = obj_data.copy()
    else:
        data = obj_data.model_dump()
    
    if user_id is not None and  hasattr(model, "user_id"):
        data["user_id"] = user_id
    
    db_obj = model(**data)
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    
    return db_obj
    
async def update(
        db: AsyncSession, 
        model, 
        obj_id: int, 
        obj_data,
        user_id: int | None = None
):
    """
    Обновляет объект модели по ID.
    
    Args:
            db: Асинхронная сессия SQLAlchemy.
            model: Класс модели SQLAlchemy.
            obj_id: ID объекта для обновления.
            obj_data: Словарь с полями для обновления.
            user_id: ID пользователя.
            
    Returns:
            Обновлённый объект или None, если объект не найден.
            
    Example:
            >>> update_data = {"title": "New Title"}
            >>> task = await update(db, models.Task, 1, update_data)
    """
    db_obj = await get_by_id(db, model, obj_id, user_id=user_id)
    
    if not db_obj:
        return None
    
    update_data = obj_data if isinstance(obj_data, dict) else obj_data.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(db_obj, key, value)
        
    await db.commit()
    await db.refresh(db_obj)
    
    return db_obj
    
async def delete(
        db: AsyncSession, 
        model, 
        obj_id: int,
        user_id: int | None = None
) -> bool:
    """
    Удаляет объект модели по ID.
    
    Args:
            db: Асинхронная сессия SQLAlchemy.
            model: Класс модели SQLAlchemy.
            obj_id: ID объекта для удаления.
            user_id: ID пользователя.
            
    Returns:
            bool: True, если объект был удалён, иначе False
    """
    db_obj = await get_by_id(db, model, obj_id, user_id=user_id)
    
    if not db_obj:
        return False
        
    await db.delete(db_obj)
    await db.commit()
    
    return True
