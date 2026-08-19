"""
Модуль содержит класс настройки базы данных Settings и 
метод получения адреса сервера базы данных.
"""

import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Класс настройки базы данных
    
    Args:
            - DB_HOST: Хост базы данных.
            - DB_PORT: Порт хоста базы данных.
            - DB_NAME: Имя базы данных.
            - DB_USER: Пользователь базы данных.
            - DB_PASSWORD: Пароль от базы данных
    """
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    
    # Параметры файла окружения
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )
    
settings = Settings()

def get_db_url():
    """Получение адресной строки сервера базы данных."""
    return (f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@"
               f"{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}")