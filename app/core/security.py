"""
Модуль содержит функции для создания и декодирования JWT-токенов.
"""

import os
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

if not SECRET_KEY:
    raise ValueError("SECRET_KEY must be set in .env file")

def create_access_token(
        data: dict, 
        expires_delta: timedelta | None = None
) -> str:
    """
    Создание JWT-токена с указаными данными и временем жизни.
    
    Args:
            - data: Данные для кодирования в токен (например, {"sub": user.email}.
            - expires_delta: Время жизни токена. Если не указано, используется ACCESS_TOKEN_EXPIRE_MINUTES.
    
    Returns:
            - str: Строка JWT-токена.
    """
    
    # Создаем копию переданных данных для токена
    to_encode = data.copy()
    
    # Определяем время жизни токена
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Добавляем в словарь дату и время окончания жизни токена    
    to_encode.update({"exp": expire})
    
    # Создаем JWT-токен
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt
    
def decode_access_token(token: str) -> dict | None:
    """
    Декодирования JWT-токена.
    
    Декодирует токен и возвращает данные, если токен валиден.
    
    Args:
            - token: Строка JWT-токена.
            
    Returns:
            dict | None: Словарь с данными из токена или None, если токен
            не валиден. 
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        return payload
    except JWTError:
        return None
