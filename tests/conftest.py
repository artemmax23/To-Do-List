"""
Модуль содержит настройки для тестирования 

Зависимости:
        - Base: Базовая модель таблицы базы данных.
        - get_db: Получение асинхронной сессии для работы с базой данных.
        - app: Экземпляр приложения.
        - get_db_url: Получение адреса работы сервера базы данных.

Настройки:
        - Создание ядра базы данных для тестирования.
        - Создание локальной сессии для работы с базой данных.
        - Создание подключения к базе данных.
        - Создание клиента для взаимодействия с API.
"""

import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from app.database import Base, get_db
from app.main import app

import uuid
from sqlalchemy import update
from app.models import User

TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"    # Адрес сервера базы данных для тестирования

# Ядро подключения к базе данных
engine = create_async_engine(
        TEST_DATABASE_URL,        # Адрес сервера базы данных
        echo=False                            # Отключение логирования SQL-запросов
)

# Фабрика асинхронных сессий
TestingSessionLocal = async_sessionmaker(
        bind=engine,                                # Ядро для подключения к базе данных
        class_=AsyncSession,                # Класс асинхронной сессии
        expire_on_commit=False,          # Объекты не будут помечены как устаревшие после вызова commit()
        autocommit=False,                    # Автоматические коммиты выключены
        autoflush=False,                         # Автоматический сброс изменений перед коммитами отключен
)

async def override_get_db():
    """Переопределённое создание сессии для работы с базой данных"""
    async with TestingSessionLocal() as session:
        yield session
        
app.dependency_overrides[get_db] = override_get_db # Переопределяем создание сессии

@pytest.fixture(scope="function", autouse=True)
async def setup_db():
    """
    Фикстура для настройки тестовой базы данных.
    
    Создаёт все таблицы перед каждым тестом и удаляет их после завершения.
    Используется автоматически (autouse=True) для всех тестов.
    
    Порядок работы:
            1. Создаёт таблицы в тестовой БД (create_all).
            2. Выполняет тест (yield).
            3. Удаляет таблицы после теста (drop_all).
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    yield
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        
@pytest.fixture(scope="function")
async def client() -> AsyncClient:
    """
    Фикстура для создания HTTP-клиента для взаимодействия с API.
    
    Returns:
        AsyncClient: Асинхронный HTTP-клиент для отправки запросов к приложению.
    """
    
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
        
@pytest.fixture(scope="function")
async def create_test_user(client: AsyncClient):
    """Создаёт тестового пользователя и вовзращает его email и пароль"""
    email = "test_user@example.com"
    password = "qwerty123"
    
    response = await client.post(
            "/auth/register",
            json={
                    "email": email,
                    "password": password 
            }
    )
    
    if response.status_code == 400:
        # Генерируем новый email
        email = f"test_{uuid.uuid4().hex[:8]}@example.com"
        response = await client.post(
                "/auth/register",
                json={
                        "email": email,
                        "password": password 
                }
        )
        
    # Активируем пользователя вручную (для тестов)
    async with TestingSessionLocal() as session:
        await session.execute(
            update(User).where(User.email == email).values(is_active=True)
        )
        await session.commit()
    
    return {"email": email, "password": password}
    
@pytest.fixture(scope="function")
async def auth_headers(client: AsyncClient, create_test_user):
    """
    Фикстура для получения заголовков с токеном авторизованного пользователя.
    """
    user = create_test_user
    
    response = await client.post(
            "/auth/login",
            data={
                    "username": user["email"],
                    "password": user["password"]
            }
    )
    
    assert response.status_code == 200, "Failed to login test user"
    access_token = response.json()["access_token"]        
    
    return {"Authorization": f"Bearer {access_token}"}