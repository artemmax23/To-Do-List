"""
Task Manager API - главный модуль приложения.

Этот модуль инициализирует FastAPI приложение, подключает роутеры,
настраивает CORS и предоставляет эндпоинты для проверки состояния сервиса.

Запуск:
    uvicorn app.main:app --reload
    
Документация:
    Swagger: /docs
    ReDoc: /redoc
"""
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.database import get_db
from app.routers import tasks, tags

# --- 1. Создание экземпряла приложения ---

app = FastAPI(
        title="Task Manager API",
        description="""
        REST API для управления задачами с тегами.
        
        ## Возможности:
        - Полный CRUD для задач и тегов
        - Пагинация и фильтрация задач
        - Поиск по названию и описанию задач
        - Автоматическая документация Swagger/ReDoc
        - Асинхронная работа с PostgreSQL через SQLAlchemy
        """,
        version="0.2.0",
        docs_url="/docs",
        redoc_url="/redoc",
        contact={
                "name": "Артём",
                "url": "https://github.com/artemmax23",
                "email": "artemmaxzolotarev@yandex.ru"
        },
        license_info={
                "name": "MIT",
                "url": "https://opensource.org/licenses/MIT",
        }
)

# --- 2. Настройка CORS ---

app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],            # В продакшене ограничь конкретными доменами
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
)

# --- 3. Подключение роутеров ---

app.include_router(tasks.router)    # Роутер для задач
app.include_router(tags.router)      # Роутер для тегов

# --- 4. Корневые эндпоинты ---

@app.get(
        "/", 
        tags=["Health Check"],
        summary="Проверка работоспособности API"
)
async def root() -> dict:
    """
    Возвращает притственое собщение и ссылки на документацию.
    
    Returns:
        dict: Сообщение о статусе, ссылки на Swagger и ReDoc.
        
    Example:
        ```http
        GET /
        ```
        
    Ans:
        ```json
        {
            "message": "Task Manager API is running",
            "docs": "/docs",
            "redoc": "/redoc"
        }
        ```
    """
    return {
            "message": "Task Manager API is running",
            "docs": "/docs",
            "redoc": "/redoc"    
    }
    
@app.get(
        "/health/db", 
        tags=["Health Check"],
        summary="Проверка подключения к базе данных"
)
async def health_check(db: AsyncSession = Depends(get_db)) -> dict:
    """
    Проверяет доступность базы данных, выполняя простой SQL-запрос.
        
    Args:
        db: Асинхронная сессия SQLAlchemy (внедряется через Depends).
        
    Returns:
        dict: Статус подключения и дополнительная информация.
        
    Raises:
        HTTPException: При ошибке подключения к БД.
        
    Example:
        ```http
        GET /health/db
        ```
        
    Ans:
        ```json
        {
                "status": "ok",
                "message": "Database connection is healthy"
        }
        ```
    """
    try:
        # Выполняем простой запрос для проверки соединения
        await db.execute(text("SELECT 1"))
        return {
                "status": "ok", 
                "mesage": "Database is connected"
        }
    except Exception as e:
        return {
                "status": "error",
                "message": f"Database connection failed: {str(e)}" 
        }