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
    text: Optional[str] = None
    state: Optional[bool] = False
    tag_id: Optional[int] = None
    
class TaskCreate(TaskBase):
    pass
    
class TaskUpdate(TaskBase):
    title: Optional[str] = None
    text: Optional[str] = None
    state: Optional[bool] = None
    tag_id: Optional[int] = None
    
class TaskResponse(TaskBase):
    id: int
    created_date: datetime
    tag: Optional[TagResponse] = None
    
    class Config:
        from_attributes = True