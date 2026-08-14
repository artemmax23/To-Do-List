from typing import Optional
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column
from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from app.database import Base
from datetime import datetime

class Tag(Base):
    __tablename__ = "tags"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    
    tasks: Mapped[Optional["Task"]] = relationship("Task", back_populates="tag_rel")
    
class Task(Base):
    __tablename__="tasks"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
            DateTime(timezone=True), 
            server_default=func.now(),
            nullable=True
    )
    
    updated_at: Mapped[Optional[datetime]] = mapped_column(
            DateTime(timezone=True),
            onupdate=func.now(),
            nullable=True
    )
    
    tag_id: Mapped[Optional[int]] = mapped_column(
            Integer,
            ForeignKey("tags.id", ondelete="SET NULL"), 
            nullable=True, 
            index=True
    )
    
    tag_rel: Mapped[Optional["Tag"]] = relationship("Tag", back_populates="tasks")