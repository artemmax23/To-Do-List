# Task Manager API

[![CI](https://github.com/artemmax23/To-Do-List/actions/workflows/ci.yml/badge.svg)](https://github.com/artemmax23/To-Do-List/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue)

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


---

## ✅ Что реализовано

### Аутентификация и безопасность
- [x] Регистрация пользователей (email + пароль)
- [x] JWT-аутентификация (access token)
- [x] Хеширование паролей (bcrypt)
- [x] Защита эндпоинтов через `get_current_user`
- [x] Изоляция данных (каждый пользователь видит только свои задачи и теги)

### Задачи
- [x] CRUD-операции (создание, чтение, обновление, удаление)
- [x] Пагинация (`page`, `limit`)
- [x] Фильтрация по статусу (`is_completed`)
- [x] Фильтрация по тегу (`tag_id`)
- [x] Поиск по названию и описанию (`search`)
- [x] Частичное обновление (PATCH)
- [x] Полное обновление (PUT)

### Теги
- [x] CRUD-операции
- [x] Поиск по точному имени
- [x] Поиск по части имени
- [x] Пагинация
- [x] Каскадное обнуление `tag_id` при удалении тега

### Архитектура
- [x] Асинхронный FastAPI + SQLAlchemy 2.0
- [x] PostgreSQL 16
- [x] Alembic-миграции
- [x] Pydantic v2 для валидации
- [x] Дженерики CRUD (base.py)
- [x] Разделение на слои (routers, crud, schemas, models)

### Инфраструктура
- [x] Docker + Docker Compose
- [x] CI/CD (GitHub Actions)
- [x] Сборка Docker-образа
- [x] Публикация в GitHub Container Registry (GHCR)
- [x] Автоматический запуск тестов при пуше

### Тестирование
- [x] Интеграционные тесты (pytest + httpx)
- [x] Покрытие: аутентификация, задачи, теги
- [x] Проверка ошибок (401, 404, 400)
- [x] Тестовая БД (SQLite + aiosqlite)

### Документация
- [x] Swagger (`/docs`) и ReDoc (`/redoc`)
- [x] Docstrings для всех модулей и функций
- [x] README с инструкциями и примерами

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

## 🎥 Демонстрация

[Смотреть скринкаст работы API](https://drive.google.com/file/d/1PtjDm8iyw_nXZvUzjgjRHHOQ6DtDCCnW/view?usp=drivesdk)

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

##Запуск через Docker

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

## 🐳 Запуск через Docker Compose

Самый простой способ запустить проект — использовать Docker Compose.

### Требования
- Docker
- Docker Compose

### Запуск

```bash
# 1. Клонируй репозиторий
git clone https://github.com/artemmax23/To-Do-List.git
cd To-Do-List

# 2. Создай файл .env (пример в .env.example)
cp .env.example .env

# 3. Запусти контейнеры
docker-compose up --build

# 4. Примени миграции (в новом терминале)
docker-compose exec app alembic upgrade head
```

### Проверка

· API: http://localhost:8000
· Swagger: http://localhost:8000/docs

### Остановка

```bash
docker-compose down
```

---

## Тестирование

### Запуск тестов:

```bash
pytest -v
```

###Покрытие тестами:

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

## Примеры запросов

### Регистрация пользователя

```http
POST /auth/register
Content-Type: application/json

{
    "email": "test@example.com",
    "password": "qwerty123"
}
```

### Логин (получение токена)

```http
POST /auth/login
Content-Type: application/x-www-form-urlencoded

username=test@example.com&password=qwerty123
```

### Создать задачу (с токеном)

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

### Получить задачи с пагинацией и фильтром

```http
GET /tasks/?page=1&limit=10&is_completed=false&search=купить
Authorization: Bearer <access_token>
```

### Обновить задачу

```http
PATCH /tasks/1
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "is_completed": true
}
```

### Создать тег

```http
POST /tags/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "name": "Личное"
}
```

---

## Структура проекта

```
To-Do-List/
├── app/
│   ├── init.py
│   ├── main.py                  # Точка входа FastAPI
│   ├── config.py                # Настройки (pydantic-settings)
│   ├── database.py              # Подключение к БД (async SQLAlchemy)
│   ├── models.py                # SQLAlchemy модели (User, Task, Tag)
│   │
│   ├── schemas/                 # Pydantic-схемы
│   │   ├── init.py
│   │   ├── user.py              # Схемы пользователя (UserCreate, UserResponse, Token)
│   │   ├── task.py              # Схемы задачи (TaskCreate, TaskUpdate, TaskResponse)
│   │   └── tag.py               # Схемы тега (TagCreate, TagUpdate, TagResponse)
│   │
│   ├── crud/                    # CRUD-операции
│   │   ├── init.py
│   │   ├── base.py              # Дженерики (get_all, get_by_id, create, update, delete)
│   │   ├── user.py              # CRUD пользователей + хеширование паролей
│   │   ├── task.py              # CRUD задач + фильтрация и поиск
│   │   └── tag.py               # CRUD тегов + поиск по имени
│   │
│   ├── routers/                 # Эндпоинты FastAPI
│   │   ├── init.py
│   │   ├── auth.py              # Регистрация, логин
│   │   ├── tasks.py             # CRUD задач
│   │   └── tags.py              # CRUD тегов
│   │
│   ├── dependencies/            # Зависимости FastAPI
│   │   ├── init.py
│   │   └── auth.py              # get_current_user (JWT)
│   │
│   └── core/                    # Ядро приложения
│       ├── init.py
│       └── security.py          # JWT: создание и декодирование токенов
│
├── migrations/                  # Alembic-миграции
│   ├── versions/                # Файлы миграций
│   ├── env.py
│   └── script.py.mako
│
├── tests/                       # Тесты (pytest)
│   ├── init.py
│   ├── conftest.py              # Фикстуры (client, auth_headers, create_test_user)
│   ├── test_auth.py             # Тесты аутентификации
│   ├── test_tasks.py            # Тесты задач
│   └── test_tags.py             # Тесты тегов
│
├── .github/
│   └── workflows/
│       └── ci.yml               # CI/CD: тесты + сборка + публикация в GHCR
│
├── .env.example                 # Пример переменных окружения
├── .gitignore                   # Игнорируемые файлы
├── Dockerfile                   # Docker-образ приложения
├── docker-compose.yml           # Docker Compose (app + PostgreSQL)
├── pytest.ini                   # Настройки pytest
├── requirements.txt             # Зависимости
└── README.md                    # Описание проекта
```

---

## 🗺️ Планы по развитию

### ✅ Реализовано
- [x] REST API для задач и тегов
- [x] JWT-аутентификация (регистрация, логин)
- [x] Изоляция данных между пользователями
- [x] Пагинация, фильтрация, поиск задач
- [x] Поиск тегов по имени
- [x] Alembic-миграции
- [x] Docker + Docker Compose
- [x] CI/CD (GitHub Actions)
- [x] Сборка и публикация Docker-образа в GHCR
- [x] Интеграционные тесты (pytest + httpx)
- [x] Swagger-документация
- [x] Полные docstrings

### 🚧 Ближайшие планы
- [ ] Экспорт задач в CSV
- [ ] Сортировка задач (`sort`, `order`)
- [ ] Дедлайны для задач
- [ ] Мягкое удаление (`is_deleted`)
- [ ] Роли пользователей (admin / user)
- [ ] Покрытие тестами 80%+ (`pytest --cov`)
- [ ] Линтеры в CI (flake8, black, isort)
- [ ] Проверка типов (mypy)
- [ ] Нагрузочное тестирование (Locust / k6)
- [ ] Замеры производительности и оптимизация запросов

### 🔮 Долгосрочные планы
- [ ] Redis для кеширования
- [ ] Celery для фоновых задач
- [ ] WebSocket для real-time уведомлений
- [ ] Prometheus + Grafana для метрик
- [ ] Sentry для отслеживания ошибок
- [ ] Деплой на Render / Railway
- [ ] Kubernetes (minikube)
- [ ] Nginx как reverse proxy
- [ ] GraphQL как альтернатива REST

---

## Автор

Артём Золотарев
GitHub: @artemmax23

---

⭐ Если проект полезен — поставь звезду на GitHub!
