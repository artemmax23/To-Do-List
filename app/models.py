"""
Модуль содержит модели таблиц базы данных

Зависимости:
        - Base: базовая модель для таблицы базы данных
        
Модели:
        - User: Модель таблицы для пользователей.
        - Tag: Модель таблицы для тегов.
        - Task: Модель таблицы для задач.
"""

from __future__ import annotations
from datetime import datetime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql import func
from sqlalchemy import Integer, String, Boolean, DateTime, ForeignKey
from app.database import Base

class User(Base):
    """
    Модель таблицы для пользователя
    
    Args:
            - id: ID пользователя, первичный ключ.
            - email: Почта пользователя (логин), уникальное поле.
            - hashed_password: Хеш пароля пользователя.
            - is_active: Статус активности пользователя.
            - created_at: Дата и время регистрации пользователя. 
    """
    
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False
    )
    
    tasks: Mapped[list[Task]] = relationship("Task", back_populates="user", cascade="all, delete-orphan")
    
    tags: Mapped[list[Tag]] = relationship("Tag", back_populates="user", cascade="all, delete-orphan")

class Tag(Base):
    """
    Модель таблицы для тегов
    
    Args:
            - id: ID тега, первичный ключ.
            - name: Имя тега.
            - user_id: ID пользователя (владельца тега).
    """
    
    __tablename__ = "tags"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    
    user_id: Mapped[int] = mapped_column(
            Integer,
            ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
            index=True
    )
    
    user: Mapped[User] = relationship("User", back_populates="tags")
    
    tasks: Mapped[list[Task]] = relationship("Task", back_populates="tag")
    
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
            - user_id: ID пользователя (владельца задачи).
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
    
    user_id: Mapped[int] = mapped_column(
            Integer,
            ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
            index=True
    )
    
    user: Mapped[User] = relationship("User", back_populates="tasks")
    
    tag: Mapped[Tag | None] = relationship("Tag", back_populates="tasks")