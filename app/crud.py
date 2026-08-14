from sqlalchemy.orm import Session
from app import models, schemas
 
 def get_all(db: Session, model, skip: int = 0, limit: int = 100):
     return db.query(model).offset(skip).limit(limit).all()
     
def get_by_id(db: Session, model, obj_id: int):
    return db.query(model).filter(model.id == obj_id).first()
    
def create(db: Session, model, obj_data):
    if isinstance(obj_data, dict):
        db_obj = model(**obj_data)
    else:
        db_obj = model(**obj_data.model_dump())
    
    db.add(db_obj)
    db.commit()
    db.refresh()
    
    return db_obj
    
def update(db: Session, model, obj_id: int, obj_data):
    db_oobj = get_by_id(db, model, obj_id)
    
    if not db_obj:
        return None
    
    update_data = obj_data if isinstance(obj_data, dict) else obj_data.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(db_obj, key, value)
        
    db.commit()
    db.refresh(db_obj)
    
    return db_obj
    
def delete(db: Session, model, obj_id: int) -> bool:
    db_obj = get_by_id(db, model, obj_id)
    
    if not db_obj:
        return False
        
    db.delete(db_obj)
    db.commit()
    
    return True
    
def get_tasks(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        is_completed: bool | None = None,
        tag_id: int | None = None
):
    query = db.query(models.Task)
    
    if is_completed is not None:
        query = query.filter(models.Task.is_completed == is_completed) 
    
    if tag_id is not None:
        query = query.filter(models.Task.tag_id == tag_id)
        
    return query.order_by(models.Task.id.desc()).offset(skip).limit(limit).all()
    
def create_task(db: Session, task: schemas.TaskCreate):
    return create(db, models.Task, task)
    
def get_task(db: Session, task_id: int):
    return get_by_id(db, models.Task, task_id)
    
def update_task(db: Session, task_id: int, task_update: schemas.TaskUpdate):
    return update(db, models.Task, task_id, task_update)
    
def delete_task(db: Session, task_id: int):
    return delete(db, models.Task, task_id)
    
def get_tags(db: Session, skip: int = 0, limit: int = 100):
    return get_all(db, models.Tag, skip, limit)
    
def get_tag(db: Session, tag_id: int):
    return get_by_id(db, models.Tag, tag_id)
    
def get_tag_by_name(db: Session, name: str):
    return db.query(models.Tag).filter(models.Tag.name == name).first()
    
def create_tag(db: Session, tag: schemas.TagCreate):
    existing_tag = get_tag_by_name(db, tag.name)
    
    if existing_tag:
        return existing_tag
        
    return create(db, models.Tag, tag)
    
def update_tag(db: Session, tag_id: int, tag_update: schemas.TagUpdate):
    return update(db, models.Tag, tag_id, tag_update)
    
def delete_tag(db: Session, tag_id: int):
    return delete(db, models.Tag, tag_id)