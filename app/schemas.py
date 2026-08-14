from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TagBase(BaseModel):
    name: str
    
class TagCreate(TagBase):
    pass
    
class TagResponse(TagBase):
    id : int
    class Config:
        from_attributes = True
        
class TaskBase(BaseModel):
    title: str
    text: str | None = None
    state: bool = False
    tag_id: int | None = None
    
class TaskCreate(TaskBase):
    pass
    
class TaskUpdate(TaskBase):
    pass
    
class TaskResponse(TaskBase):
    id: int
    created_date: datetime
    updated_at: datetime | None
    tag_id: int | None = None
    
    class Config:
        from_attributes = True