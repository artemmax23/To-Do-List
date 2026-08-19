"""
Модуль содержит модели таблиц базы данных

Зависимости:
        - Base: базовая модель для таблицы базы данных
        
Модели:
        - Tag: модель таблицы для тегов.
        - Task: модель таблицы для задач.
"""

from __future__ import annotations
from datetime import datetime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql import func
from sqlalchemy import Integer, String, Boolean, DateTime, ForeignKey
from app.database import Base

class Tag(Base):
    """
    Модель таблицы для тегов
    
    Args:
            - id: ID тега, первичный ключ.
            - name: Имя тега. 
    """
    
    __tablename__ = "tags"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    
    tasks: Mapped[Task | None] = relationship("Task", back_populates="tag_rel")
    
class Task(Base):
    """
    Модель таблицы для задач
    
    Args:
            - id: ID задачи, первичный ключ.
            - title: Заголовок задачи.
            - description: Описание задачи.
            - is_completed: Статус выполнения задачи.
            - created_at: Дата и время создания задачи.
            - updated_at: Дата и время последнего обновления задачи.
            - tag_id: ID тега, внешний ключ, связь с таблицей tags.
    """
    
    __tablename__ = "tasks"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
            DateTime(timezone=True), 
            server_default=func.now(),
            nullable=False
    )
    
    updated_at: Mapped[datetime | None] = mapped_column(
            DateTime(timezone=True),
            onupdate=func.now(),
            nullable=True
    )
    
    tag_id: Mapped[int | None] = mapped_column(
            Integer,
            ForeignKey("tags.id", ondelete="SET NULL"), 
            nullable=True, 
            index=True
    )
    
    tag_rel: Mapped[Tag | None] = relationship("Tag", back_populates="tasks")