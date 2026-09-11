# Task Manager API

[![CI](https://github.com/artemmax23/To-Do-List/actions/workflows/ci.yml/badge.svg)](https://github.com/artemmax23/To-Do-List/actions/workflows/ci.yml)

REST API для управления задачами с тегами, пользователями и JWT-аутентификацией.

Проект написан на **FastAPI** с использованием асинхронной **PostgreSQL** через **SQLAlchemy 2.0**.
Поддерживает полный CRUD для задач и тегов, пагинацию, фильтрацию, поиск и изоляцию данных между пользователями.

---

## Содержание

- [Технологии](#технологии)
- [Возможности API](#возможности-api)
- [Запуск проекта](#запуск-проекта)
- [Запуск через Docker](#запуск-через-docker)
- [Тестирование](#тестирование)
- [Примеры запросов](#примеры-запросов)
- [Структура проекта](#структура-проекта)
- [Планы по развитию](#планы-по-развитию)

---

## Технологии

- **FastAPI** — веб-фреймворк
- **SQLAlchemy 2.0** — асинхронный ORM
- **PostgreSQL** — реляционная база данных
- **Alembic** — миграции
- **Pydantic** — валидация данных
- **JWT (python-jose)** — аутентификация
- **passlib (bcrypt)** — хеширование паролей
- **Docker** + **Docker Compose** — контейнеризация
- **Pytest + httpx** — тестирование
- **Uvicorn** — ASGI сервер

---

## Возможности API

### Аутентификация (`/auth`)
- `POST /auth/register` — регистрация пользователя
- `POST /auth/login` — логин (получение JWT-токена)

### Задачи (`/tasks`)
- `GET /tasks/` — список задач (пагинация, фильтрация по статусу, тегу и поиск по названию/описанию)
- `POST /tasks/` — создание задачи
- `GET /tasks/{id}` — получение задачи по ID
- `PATCH /tasks/{id}` — частичное обновление задачи
- `PUT /tasks/{id}` — полное обновление задачи
- `DELETE /tasks/{id}` — удаление задачи

### Теги (`/tags`)
- `GET /tags/` — список тегов (пагинация)
- `POST /tags/` — создание тега
- `GET /tags/{id}` — получение тега по ID
- `GET /tags/name/{name}` — поиск тега по имени
- `GET /tags/search/{search}` — поиск тегов по части имени
- `PUT /tags/{id}` — обновление тега
- `DELETE /tags/{id}` — удаление тега (с автоматическим обнулением в задачах)

### Особенности
- **JWT-аутентификация** — все эндпоинты защищены
- **Изоляция данных** — каждый пользователь видит только свои задачи и теги
- **Пагинация, фильтрация, поиск** — для задач
- **Валидация** — через Pydantic

---

## Запуск проекта

### Локально (без Docker)

1. **Клонируй репозиторий:**
   ```bash
   git clone https://github.com/artemmax23/To-Do-List.git
   cd To-Do-List
```

2. Создай и активируй виртуальное окружение:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows
   ```
3. Установи зависимости:
   ```bash
   pip install -r requirements.txt
   ```
4. Создай файл .env (на основе .env.example):
   ```env
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=task_db
   DB_USER=user
   DB_PASSWORD=password
   ```
5. Создай базу данных и примени миграции:
   ```bash
   createdb task_db -U user
   alembic upgrade head
   ```
6. Запусти сервер:
   ```bash
   uvicorn app.main:app --reload
   ```
7. Открой документацию:
   http://localhost:8000/docs

---

Запуск через Docker

Убедись, что у тебя установлены Docker и Docker Compose.

1. Собери и запусти контейнеры:
   ```bash
   docker-compose up --build
   ```
2. Примени миграции (внутри контейнера):
   ```bash
   docker-compose exec app alembic upgrade head
   ```
3. Готово!
   · API доступно по адресу: http://localhost:8000
   · Swagger документация: http://localhost:8000/docs

---

Тестирование

Запуск тестов:

```bash
pytest -v
```

Покрытие тестами:

Аутентификация:

· Регистрация пользователя
· Успешный логин
· Неверный пароль / email
· Дублирование email
· Доступ к защищённым эндпоинтам без/с невалидным токеном

Задачи:

· Создание задачи
· Создание задачи с тегом
· Создание задачи с несуществующим тегом
· Получение пустого списка
· Получение задачи по ID
· Обновление задачи (PATCH)
· Удаление задачи
· Фильтрация по статусу is_completed
· Поиск по тексту
· Изоляция данных (пользователь не видит задачи другого)

Теги:

· Создание тега
· Получение пустого списка
· Получение тега по ID
· Получение тега по имени
· Поиск тегов по части имени
· Обновление тега
· Удаление тега

---

Примеры запросов

Регистрация пользователя

```http
POST /auth/register
Content-Type: application/json

{
    "email": "test@example.com",
    "password": "qwerty123"
}
```

Логин (получение токена)

```http
POST /auth/login
Content-Type: application/x-www-form-urlencoded

username=test@example.com&password=qwerty123
```

Создать задачу (с токеном)

```http
POST /tasks/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "title": "Купить продукты",
    "description": "Молоко, хлеб, яйца",
    "tag_id": 1
}
```

Получить задачи с пагинацией и фильтром

```http
GET /tasks/?page=1&limit=10&is_completed=false&search=купить
Authorization: Bearer <access_token>
```

Обновить задачу

```http
PATCH /tasks/1
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "is_completed": true
}
```

Создать тег

```http
POST /tags/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "name": "Личное"
}
```

---

Структура проекта

```
task_manager/
├── app/
│   ├── __init__.py
│   ├── main.py              # Точка входа
│   ├── config.py            # Настройки (pydantic-settings)
│   ├── database.py          # Подключение к БД
│   ├── models.py            # SQLAlchemy модели (User, Task, Tag)
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py          # Pydantic схемы пользователя
│   │   ├── task.py          # Pydantic схемы задачи
│   │   └── tag.py           # Pydantic схемы тега
│   ├── crud/
│   │   ├── __init__.py
│   │   ├── base.py          # Дженерики CRUD
│   │   ├── user.py          # CRUD пользователей
│   │   ├── task.py          # CRUD задач
│   │   └── tag.py           # CRUD тегов
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── auth.py          # Эндпоинты аутентификации
│   │   ├── tasks.py         # Эндпоинты задач
│   │   └── tags.py          # Эндпоинты тегов
│   ├── dependencies/
│   │   ├── __init__.py
│   │   └── auth.py          # get_current_user
│   └── core/
│       ├── __init__.py
│       └── security.py      # JWT (создание/декодирование)
├── migrations/              # Alembic миграции
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Фикстуры
│   ├── test_auth.py         # Тесты аутентификации
│   ├── test_tasks.py        # Тесты задач
│   └── test_tags.py         # Тесты тегов
├── .env.example             # Пример переменных окружения
├── .gitignore               # Игнорируемые файлы
├── Dockerfile               # Docker образ
├── docker-compose.yml       # Docker Compose
├── pytest.ini               # Настройки тестов
├── requirements.txt         # Зависимости
└── README.md                # Описание проекта
```

---

Планы по развитию

☑ Добавить аутентификацию (JWT)
☑ Поддержка пользователей и личных задач
☑ Написать интеграционные тесты для всех сущностей
☐ Экспорт задач в CSV
☐ Уведомления о дедлайнах
☐ Внедрение Redis для кеширования
☐ CI/CD через GitHub Actions
☐ Нагрузочное тестирование (Locust)

---

Автор

Артём Золотарев
GitHub: @artemmax23

---

⭐ Если проект полезен — поставь звезду на GitHub!
