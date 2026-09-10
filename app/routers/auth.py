"""
Маршруты (роутеры) для работы с пользователями.

Предоставляет набор эндпоинтов для регистрации и авторизации пользователя:
- Регистрация (POST /auth/register)
- Авторизация (POST /auth/login)

Все эндпоинты используют асинхронные сессии SQLAlchemy и валидацию через Pydantic
Автоматическая документация доступна в Swagger (/docs) и ReDoc (/redoc)

Зависимости:
        - get_db: внедряет асинхронную сессию базы данных.
        - crud: функции для работы с базой данных.
        - schemas: Pydantic-схемы для валидации запросов и ответов.
        - create_access_token: Создание JWT-токена.
        - ACCESS_TOKEN_EXPIRES_MINUTES: Время действия JWT-токена в минутах.
        
Пример:
        # Регистрация пользователя
        ```http
         POST /auth/register
        Content-Type: application/json
        
        {
                   "email": "example@mail.com",
                   "password": "123"
         }
        ```

Ответ:
        ```json
        {
                "id": 1,
                "email": "example@mail.com",
                "is_active": false,
                "created_at": "2026-08-20T10:00:00+00:00"
        }
        ```
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta
from app import crud, schemas
from app.database import get_db
from app.core.security import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post(
        "/register", 
        status_code=status.HTTP_201_CREATED,
        response_model=schemas.UserResponse
)
async def register(
        user_data: schemas.UserCreate, 
        db: AsyncSession = Depends(get_db)
):
    """
    Регистрация пользователя.
    
    Args:
            - user_data: Данные пользователя для регистрации (email, password).
            - db: Асинхронная сессия SQLAlchemy.
    
    Returns:
            schemas.UserResponse: Объект пользователя с полями id, email, is_active и created_at.  
            
    Raises:
            HTTPException: 400, если пользователь с таким email существует.   
                            
    Example:
            ```http
            POST /auth/register
            Content-Type: application/json
            
            {
                       "email": "example@mail.com",
                       "password": "123"
             }
            ```
            
    Response:
            ```json
            {
                    "id": 1,
                    "email": "example@mail.com",
                    "is_active": false,
                    "created_at": "2026-08-20T10:00:00+00:00"
            }
            ```
    """
    
    existing_user = await crud.get_user_by_email(db, user_data.email)
    
    if existing_user:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
        )
        
    return await crud.create_user(db, user_data)
    
@router.post("/login", response_model=schemas.Token)
async def login(
        user_data: OAuth2PasswordRequestForm = Depends(), 
        db: AsyncSession = Depends(get_db)
):
    """
    Авторизация пользователя.
    
    Args:
            - user_data: Данные пользователя для авторизации (email, password).
            - db: Асинхронная сессия SQLAlchemy.
    
    Returns:
            schemas.Token: Объект JWT-токена с полями access_token и token_type.  
            
    Raises:
            HTTPException: 401, если email или пароль пользователя некорректны.
                            
    Example:
            ```http
            POST /auth/login
            Content-Type: application/json
            
            {
                       "email": "example@mail.com",
                       "password": "123"
             }
            ```
            
    Response:
            ```json
            {
                    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                    "token_type": "bearer"
            }
            ```
    """
    
    user = await crud.authenticate_user(db, user_data.username, user_data.password)
    
    if not user:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
        )
        
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}