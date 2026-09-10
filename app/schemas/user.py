"""
Модуль содержит Pydantic-схемы для валидации запросов и ответов по пользователям.

Схемы валидации для пользователя:
        - UserBase: Базовая схема с общими полями.
        - UserCreate: Схема для создания пользователя.
        - UserPatch: Схема для чаcтичного обновления пользователя. 
        - UserResponse: Схема ответа для пользователя (c id, is_active, created_at).
        - Token: Схема для ответа с JWT-токеном при успешной аутентификации.
        - TokenData: Схема для хранения данных, закодированных в JWT-токене.
"""

from pydantic import BaseModel, ConfigDict, EmailStr, Field
from datetime import datetime
                        
class UserBase(BaseModel):
    """
    Базовая схема с общими полями для пользователя
    
    Args:
            - email: Почта пользователя (логин).
    """
    email: EmailStr
    
class UserCreate(UserBase):
    """
    Схема для создания пользователя.
    
    Args:
            - password: Пароль пользователя.
    """
    password: str = Field(..., min_length=8, max_length=72, description="Пароль 8-72 символа")

class UserPatch(BaseModel):
    """
    Схема для частичного обновления пользователя
    
    Все аргументы данной схемы опциональны.
    
    Args:
            - email: Почта пользователя (логин).
            - password: Пароль пользователя.
    """
    email: EmailStr | None = None
    password: str | None = None       
            
class UserResponse(UserBase):
    """
    Схема ответа для пользователя (c id, is_active, created_at).
    
    Args:
            - id: ID пользователя.
            - is_active: Статус пользователя (True - активен, False - заблокирован).
            - created_at: Дата и время регистрации пользователя.
    """
    id: int
    is_active: bool
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True) # Превращает SQLAlchemy-объект в JSON
    
class Token(BaseModel):
    """
    Схема для ответа с JWT-токеном при успешной аутентификации.
    
    Args:
            - access_token: Строка JWT-токена.
            - token_type: Тип токена (всегда "bearer" для стандарта OAuth2).
    """
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    """
    Схема для хранения данных, закодированных в JWT-токене.
    
    Args:
            - email: Почта пользователя (субъект токена). Может быть None, если
            токен повреждён.
    """
    email: str | None = None