"""
Модуль описывает зависимость для получения текущего пользователя

Зависимости:
        - models: Модели таблиц.
        - schemas: Pydantic-схемы для валидации.
        - crud: CRUD операции.
        - get_db: Получение сессии для работы с базой данных.
        - decode_access_token: Декодирование access-токена
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError
from app import crud, schemas, models
from app.database import get_db
from app.core.security import decode_access_token

# Создание зависимости для извлечения токена из заголовка Authorization
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: AsyncSession = Depends(get_db)
) -> models.User:
    """
    Получение текущего пользователя из JWT-токена
    
    Декодирует токен, извлекает email пользователя и возвращает объект пользователя.
    Если токен невалиден, пользователь не найден или email отсутствует -
    выбрасывается HTTPException с кодом 401.
    
    Args: 
            - token: JWT-токен из заголовка Authorization.
            - db: Асинхронная сессия SQLAlchemy.
            
    Returns:
            models.User: Объект текущего пользователя.
            
    Raises:
        HTTPException: 401, Unauthorized - если токен невалиден,
                                     пользователь не найден или email отсутствует.
    """
    
    credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception
        
    email: str = payload.get("sub")
    if email is None:
        raise credentials_exception
        
    user = await crud.get_user_by_email(db, email)
    if user is None:
        raise credentials_exception
        
    return user