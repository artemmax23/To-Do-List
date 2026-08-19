# Task Manager API

REST API для упавления задачами с тегами

Проект написан на **FastAPI** с использованием асинхронной **PostgresSQL** через **SQLAlchemy**.
Поддерживает полный CRUD для задач и тегов, пагинацию, фильтрацию и поиск.

---

## Содержание

- [Технологии](#технологии)
- [Возможности API](#возможности-api)
- [Запуск проекта](#запуск-проекта)
- [Запуск через Docker](#запуск-через-docker)
- [Тестирование](#тестироование)
- [Примеры запросов](#примеры-запросов)
- [Структура проекта](#структура-проекта)
- [Планы по развитию](#планы-по-развитию)

---

## Технологий

- **FastAPI** - веб-фреймворк
- **SQLAlchemy 2.0** - асинхронный ORM
- **PostgreSQL** - реляционная база данных
- **Alembic** - миграции
- **Pydantic** - валидация данных
- **Docker** + **Docker Compose** - контейнеризация
- **Pytest** - тестирование
- **Uvicorn** - ASGI сервер

---

## Возможности API

### Задачи (`/tasks`) 
- `GET /tasks` - список задач (пагинация, фильтрация по статусу, тегу и поиск по названию
- `POST /tasks` - создание задачи
- `GET /tasks/{id}` - получение задачи по ID
- `PATCH /tasks/{id}` - частичное обновление задачи
- `PUT /tasks/{id}` - полное обновление задачи
- `DELETE /tasks/{id}` - удаление задачи

### Теги (`/tags`)
- `GET /tags` - список тегов (пагинация)
- `POST /tags` - создание тегов
- `GET /tags/{id}` - получение тега по ID
- `GET /tags/name/{name}` - поиск тега по имени
- `PUT /tags/{id}` - обновление тега
- `DELETE /tags/{id}` - удаление тега (с автоматическим обнулением в задачах)

---

## Запуск проекта

### Локально (без Docker)

1. **Клонируй репозиторий:**
 ```bash
 git clone https://github.com/artemmax23/To-Do-List.git
 cd To-Do-List
 ```

2. **Создай и активируй виртуальное окружение:**
 ```bash
 python -m venv venv
 source venv/bin/activate # Linux/macOS
 venv\Scripts\activate    # Windows
 ```

3. **Установи зависимости:**
 ```bash
 pip install -r requirements.txt
 ```

4. **Создай файл .env (на основе .env.example):**
 ```env
 DB_HOST=localhost
 DB_PORT=5432
 DB_NAME=task_db
 DB_USER=user
 DB_PASSWORD=password
 ```

5. **Создай базу данных и примени миграции:**
 ```bash
 creatdb task_db -U user
 alembic upgrade head
 ```

6. **Запусти сервер:**
 ```bash
 uvicorn ap.main:app --reload
 ```

7. **Открой документацию:**
   http://localhost:8000/docs

## Запуск через Docker

**Убедись, что у тебя установлены Docker и Docker Compose.**

1. **Собери и запусти контейнеры:**
 ```bash
 docker-compose up --build
 ```

2. **Примени миграции (внутри контейнера):**
 ```bash
 docker-compose exec app alembic upgrade head
 ```

3. **Готово!**
  API доступно по адресу: http://localhost:8000
  Swagger документация: http://localhost:8000/docs

---

## Тестирование

### Запуск тестов:

```bash
pytest -v
```

### Покрытие тестами:

· Создание задачи и тега
· Получение списка с пагинацией
· Обновление и удаление
· Проверка ошибок (404, 422)

---

## Примеры запросов

### Создать задачу

```http
POST /tasks/
Content-Type: application/json

{
    "title": "Купить продукты",
    "description": "Молоко, хлеб, яйца",
    "tag_id": 1
}
```

### Получить задачи с пагинацией и фильтром

```http
GET /tasks?page=1&limit=10&is_completed=false&search=купить
```

### Обновить задачу

```http
PATCH /tasks/1
Content-Type: application/json

{
    "is_completed": true
}
```

### Создать тег

```http
POST /tags/
Content-Type: application/json

{
    "name": "Личное"
}
```

---

## Структура проекта

```
task_manager/
├── app/
│   ├── __init__.py
│   ├── main.py              # Точка входа
│   ├── config.py            # Настройки
│   ├── database.py          # Подключение к БД
│   ├── models.py            # SQLAlchemy модели
│   ├── schemas.py           # Pydantic схемы
│   ├── crud.py              # CRUD функции
│   └── routers/
│       ├── tasks.py         # Эндпоинты задач
│       └── tags.py          # Эндпоинты тегов
├── migrations/              # Alembic миграции
├── tests/                   # Pytest тесты
├── .env.example             # Пример переменных окружения
├── .gitignore               # Игнорируемые файлы
├── Dockerfile               # Docker образ
├── docker-compose.yml       # Docker Compose
├── requirements.txt         # Зависимости
└── README.md                # Описание проекта
```

---

## Планы по развитию

☐ Добавить аутентификацию (JWT)
☐ Поддержка пользователей и личных задач
☐ Экспорт задач в CSV
☐ Уведомления о дедлайнах
☐ Внедрение Redis для кеширования
☐ CI/CD через GitHub Actions
☐ Нагрузочное тестирование (Locust)

---

Автор

Артём
GitHub: @artemmax23

---

⭐ Если проект полезен — поставь звезду на GitHub!
