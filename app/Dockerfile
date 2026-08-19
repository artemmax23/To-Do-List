# 1. Загружаем базовый образ Python 3.11 (slim-версия)
FROM python:3.11-slim

# 2. Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# 3. Копируем файл с зависимостями
COPY requirements.txt .

# 4. Устанавливаем зависимости 
RUN pip install --no-cache-dir -r requirements.txt

# 5. Копируем весь код проекта
COPY . .

# 6. Команда для запуска приложения
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]