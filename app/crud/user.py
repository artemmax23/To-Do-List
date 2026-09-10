"""
Специализированные CRUD операции для пользователей (User).

Содержит функции для регистрации и авторизации пользователей (User). 
Все асинхронные функции принимают сессию SQLAlchemy в качестве первого аргумента.

Зависимости:
        - models: Модели таблиц.
        - schemas: Pydantic-схемы для валидации.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from passlib.context import CryptContext
from app import models, schemas

pwd_context = CryptContext(
        schemes=["bcrypt"], 
        deprecated="auto"
)

def verify_password(
        plain_password: str,
        hashed_password: str
) -> bool:
    """
    Проверка совпадения паролей.
    
    Args:
            - plain_password: Введённый пароль.
            - hashed_password: Хеш правильного пароля.
            
    Returns:
            bool: Возвращает True, если пароли совпадают, иначе False.
    """
    return pwd_context.verify(plain_password, hashed_password)
    
def get_password_hash(password: str) -> str:
    """
    Возвращает хеш для пароля.
    
    Args:
            - password: Введённый пароль.
            
    Returns:
            str: Хеш переданного пароля.
    """
    return pwd_context.hash(password)
    
async def get_user_by_email(
        db: AsyncSession,
        email: str
) -> models.User | None:
    """
    Получение пользователя по его почте.
    
    Args:
            - db: Асинхронная сессия SQLAlchemy.
            - email: электронная почта (логин) пользователя.
            
    Returns:
            models.User | None: Возвращает объект пользователя или None.
    """
    result = await db.execute(
            select(models.User).where(models.User.email == email)
    )
    
    return result.scalar_one_or_none()
    
async def create_user(
        db: AsyncSession,
        user_data: schemas.UserCreate
) -> models.User:
    """
    Создание пользователя.
    
    Args:
            - db: Асинхронная сессия SQLAlchemy.
            - user_data: Данные для создания пользователя (email, password).
            
    Returns:
            models.User: Возвращает объект пользователя.
    """
    
    print(len(user_data.password))
    
    # Получение хеша пароля
    hashed_password = get_password_hash(user_data.password)
    
    new_user = models.User(
            email=user_data.email,
            hashed_password=hashed_password
    )
    
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    return new_user
    
async def authenticate_user(
        db: AsyncSession,
        email: str,
        password: str
) -> models.User | None:
    """
    Авторизация пользователя.
    
    Args:
            - db: Асинхронная сессия SQLAlchemy.
            - email: Электронная почта (логин) пользователя.
            - password: Пароль пользователя.
            
    Returns:
            models.User | None: Возвращает объект пользователя или None.
    """
    
    user = await get_user_by_email(db, email)
    
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None   
    return user
