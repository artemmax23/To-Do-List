from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from app.database import Base

class Tag(Base):
    __tablename__ = "tags"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True, index=True)
    
    tasks = relationship("Task", back_populates="tag_rel")
    
class Task(Base):
    __tablename__="tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    text = Column(String, nullable=True)
    state = Column(Boolean, default=False)
    created_date = Column(DateTime(timezone=True), server_default=func.now())
    
    tag_id = Column(Integer, ForeignKey("tags.id"), nullable=True, index=True)
    
    tag_rel = relationship("Tag", back_populates="tasks")
