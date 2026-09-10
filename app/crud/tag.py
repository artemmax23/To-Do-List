"""
Специализированные CRUD операции для тегов (Tag).

Содержит функции для создания, чтения, обновления и удаления
тегов (Tag). Все функции асинхронны и принимают сессию SQLAlchemy 
в качестве первого аргумента.

Зависимости:
        - models: Модели таблиц.
        - schemas: Pydantic-схемы для валидации.
        - crud: CRUD операции. Нужен для дженериков.
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app import models, schemas
from app.crud import base
from app.dependencies.auth import get_current_user
            
async def get_tags(
        db: AsyncSession, 
        user_id: int,
        skip: int = 0, 
        limit: int = 100, 
) -> list[models.Tag]:
    """Возвращает список тегов с пагинацией."""
    return await base.get_all(db, models.Tag, skip, limit, user_id)
    
async def get_tag(
        db: AsyncSession, 
        user_id: int,
        tag_id: int, 
) -> models.Tag | None:
    """Возвращает тег по ID или None."""
    return await base.get_by_id(db, models.Tag, tag_id, user_id)

async def get_tag_by_name(
        db: AsyncSession,
        user_id:int, 
        search: str, 
) -> models.Tag | None:
    """
    Возвращает тег по имени (регистрозависимо)
    
    Args:
           - db: Асинхронная сессия SQLAlchemy.
           - user_id: ID пользователя.
           - search: Часть названия тега.
            
    Returns:
            models.Tag | None: Объект тега или None, если не найден. 
    """     
    result = await db.execute(
            select(models.Tag)
            .where(models.Tag.user_id == user_id)
            .where(models.Tag.name.ilike(search))
    )
    
    return result.scalar_one_or_none()    
            
async def get_tags_by_search(
        db: AsyncSession, 
        user_id:int,
        search: str, 
        skip: int = 0, 
        limit: int = 100,
) -> list[models.Tag]:
    """
    Возвращает список тегов по имени (регистронезависимо)
    
    Args:
            - db: Асинхронная сессия SQLAlchemy.
            - user_id: ID пользователя.
            - search: Часть названия тега.
            - skip: Количество записей для пропуска.
            - limit: Максимальное колиество записей.
            
    Returns:
            list[models.Tag]: Список тегов, содержащих подстроку в названии:
                
    Example:
            >>> tags = await get_tags_by_search(db, "работ", skip=0, limit=10) 
    """
    result = await db.execute(
            select(models.Tag)
            .where(models.Tag.user_id == user_id)
            .where(models.Tag.name.ilike(f"%{search}%"))
            .offset(skip)
            .limit(limit)
    )
    
    return result.scalars().all()
    
async def create_tag(
        db: AsyncSession, 
        user_id: int,
        tag: schemas.TagCreate
) -> models.Tag:
    """Создаёт новый тег. Если тег с таким именем существует, возвращает его"""
    existing_tag = await get_tag_by_name(db, user_id, tag.name)
    
    if existing_tag:
        return existing_tag
        
    return await base.create(db, models.Tag, tag, user_id)
    
async def update_tag(
        db: AsyncSession,
        user_id: int, 
        tag_id: int, 
        tag_update: schemas.TagUpdate | dict,
) -> models.Tag | None:
    """Обновляет тег по ID. Принимает схему или словарь"""
    return await base.update(db, models.Tag, tag_id, tag_update, user_id)
    
async def delete_tag(
        db: AsyncSession,
        user_id: int,
        tag_id: int
 ) -> bool:
    """Удаляет тег по ID."""
    return await base.delete(db, models.Tag, tag_id, user_id)
