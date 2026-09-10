"""
Модуль содержит Pydantic-схемы для валидации запросов и ответов по задачам.

Схемы валидации для задач:
        - TaskBase: Базовая схема с общими полями.
        - TaskCreate: Схема для создания задачи.
        - TaskUpdate: Схема для полного обновления задачи.
        - TaskPatch: Схема для частичного обновления задачи. 
        - TaskResponse: Схема ответа (c id, created_at, updated_at).
"""

from pydantic import BaseModel, ConfigDict
from datetime import datetime
                        
class TaskBase(BaseModel):
    """
    Базовая схема с общими полями для задачи
    
    Args:
            - title: Заголовок задачи.
            - description: Описание задачи (опционально).
            - is_completed: Статус задачи.
            - tag_id: ID тега (опционально).
    """
    title: str
    description: str | None = None
    is_completed: bool = False
    tag_id: int | None = None
    
class TaskCreate(TaskBase):
    """Схема для создания задачи."""
    pass
    
class TaskUpdate(TaskBase):
    """Схема для полного обновления задачи"""
    pass

class TaskPatch(BaseModel):
    """
    Схема для частичного обновления задачи
    
    Все аргументы данной схемы опциональны.
    
    Args:
            - title: Заголовок задачи.
            - description: Описание задачи.
            - is_completed: Статус задачи.
            - tag_id: ID тега.
    """
    title: str | None = None
    description: str | None = None
    is_completed: bool | None = None
    tag_id: int | None = None        
            
class TaskResponse(TaskBase):
    """
    Схема ответа для задачи (c id, created_at, updated_at).
    
    Args:
            - id: ID задачи.
            - created_at: Дата и время создания задачи.
            - updated_at: Дата и время последнего изменения задачи.
            - tag_id: ID тега.
    """
    id: int
    created_at: datetime
    updated_at: datetime | None
    tag_id: int | None = None
    
    model_config = ConfigDict(from_attributes=True) # Превращает SQLAlchemy-объект в JSON