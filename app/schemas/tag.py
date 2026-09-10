"""
Модуль содержит Pydantic-схемы для валидации запросов и ответов по тегам.

Схемы валидации для тегов:
        - TagBase: Базовая схема с общими полями.
        - TagCreate: Схема для создания тега.
        - TagUpdate: Схема для обновления тега.
        - TagResponse: Схема ответа (с id).
"""

from pydantic import BaseModel, ConfigDict
from datetime import datetime

class TagBase(BaseModel):
    """
    Базовая схема с общими полями для тега
    
    Args:
            - name: Название тега.
    """
    name: str
    
class TagCreate(TagBase):
    """Схема для создания тега."""
    pass
    
class TagResponse(TagBase):
    """
    Схема ответа для тега (с id)
    
    Args:
            - id: ID тега.
    """
    id: int
     
    model_config = ConfigDict(from_attributes=True) # Превращает SQLAlchemy-объект в JSON

class TagUpdate(TagBase):
    """Схема обновления тега."""
    pass
    