from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app import models, schemas
 
async def get_all(db: AsyncSession, model, skip: int = 0, limit: int = 100):
     result = await db.execute(
             select(model).offset(skip).limit(limit).all()
     )
     
     return result.scalars().all()
     
async def get_by_id(db: AsyncSession, model, obj_id: int):
    result = await db.execute(
        select(model).where(model.id == obj_id)
    )
    
    return result.scalar_one_or_none()
    
async def create(db: AsyncSession, model, obj_data):
    if isinstance(obj_data, dict):
        db_obj = model(**obj_data)
    else:
        db_obj = model(**obj_data.model_dump())
    
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    
    return db_obj
    
async def update(db: AsyncSession, model, obj_id: int, obj_data):
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
    db_obj = await get_by_id(db, model, obj_id)
    
    if not db_obj:
        return False
        
    await db.delete(db_obj)
    await db.commit()
    
    return True
    
async def get_tasks(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100,
        is_completed: bool | None = None,
        tag_id: int | None = None,
        search: str | None = None
) -> list[models.Task]:
    query = select(models.Task)
    
    if is_completed is not None:
        query = query.where(models.Task.is_completed == is_completed) 
    
    if tag_id is not None:
        query = query.where(models.Task.tag_id == tag_id)
        
    if search:
            query = query.where(
                    (models.Task.title.ilike(f"%{search}%")) |
                    (models.Task.description.ilike(f"%{search}%"))
            )    
    
    query = query.offset(skip).limit(limit).order_by(models.Task.id.desc())
    result = await db.execute(query)            
                                        
    return result.scalars().all()
    
async def create_task(db: AsyncSession, task: schemas.TaskCreate):
    return await create(db, models.Task, task)
    
async def get_task(db: AsyncSession, task_id: int):
    return await get_by_id(db, models.Task, task_id)
    
async def update_task(db: AsyncSession, task_id: int, task_update: schemas.TaskUpdate):
    return await update(db, models.Task, task_id, task_update)
    
async def delete_task(db: AsyncSession, task_id: int):
    return await delete(db, models.Task, task_id)
    
async def get_tags(db: AsyncSession, skip: int = 0, limit: int = 100):
    return await get_all(db, models.Tag, skip, limit)
    
async def get_tag(db: AsyncSession, tag_id: int):
    return await get_by_id(db, models.Tag, tag_id)
    
async def get_tag_by_name(db: AsyncSession, name: str):
    result = await db.execute(
            select(models.Tag).filter(models.Tag.name == name)
    )
    
    return result.scalar_one_or_none()
    
async def create_tag(db: AsyncSession, tag: schemas.TagCreate):
    existing_tag = await get_tag_by_name(db, tag.name)
    
    if existing_tag:
        return existing_tag
        
    return await create(db, models.Tag, tag)
    
async def update_tag(db: AsyncSession, tag_id: int, tag_update: schemas.TagUpdate):
    return await update(db, models.Tag, tag_id, tag_update)
    
async def delete_tag(db: AsyncSession, tag_id: int):
    return await delete(db, models.Tag, tag_id)