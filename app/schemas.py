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

class TagUpdate(TagBase):
    pass        
                        
class TaskBase(BaseModel):
    title: str
    description: str | None = None
    is_completed: bool = False
    tag_id: int | None = None
    
class TaskCreate(TaskBase):
    pass
    
class TaskUpdate(TaskBase):
    pass

class TaskPatch(BaseModel):
    title: str | None
    description: str | None = None
    is_completed: bool | None = False
    tag_id: int | None = None        
            
class TaskResponse(TaskBase):
    id: int
    created_at: datetime
    updated_at: datetime | None
    tag_id: int | None = None
    
    class Config:
        from_attributes = True