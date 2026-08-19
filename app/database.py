"""
Модуль отвечает за создание сессии для работы с базой данных

Зависимости:
        - get_db_url: получения адреса сервера базы данных.
"""

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, declared_attr
from app.config import get_db_url

DATABASE_URL = get_db_url() # Ссылка на базу данных

# Ядро подключения к базе данных
engine = create_async_engine(
        DATABASE_URL,            # 1. Строка подключения к базе данных
        echo=True,                      # 2. Логирование SQL-запросов
        pool_pre_ping=True,      # 3. Проверка соединения перед использованием
)

# Фабрика асинхронных сессий
async_session_maker = async_sessionmaker(
        bind=engine,                            # 1. Ядро подключения к базе данных
        class_=AsyncSession,            # 2. Класс асинхронной сессии
        expire_on_commit=False       # 3. Объекты не будут помечены как устаревшие после вызова commit()
)

class Base(DeclarativeBase):
    """Абстрактный базовый класс для таблиц базы данных."""
    
    __abstract__ = True
    
    @declared_attr
    def __tablename__(cls) -> str:
        """Получение имени таблицы."""
        return f"{cls.__name__.lower()}s"
        
async def get_db() -> AsyncSession:
    """Создание сессии для работы с базой данных"""
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
    