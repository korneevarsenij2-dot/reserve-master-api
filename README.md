# 🍽️ ReserveMaster API — Сервис бронирования столов

Асинхронный RESTful API сервис для управления рестораном и резервирования столов с защитой от состояния гонки (Race Condition), JWT-аутентификацией, кэшированием и автотестами.

---

## 🚀 Стек технологий

* **Язык:** Python 3.9+ / 3.11+
* **Фреймворк:** FastAPI (асинхронный)
* **База данных:** PostgreSQL + SQLAlchemy 2.0 (AsyncSession) + asyncpg
* **Миграции:** Alembic
* **Кэширование:** Redis
* **Безопасность:** JWT (JSON Web Tokens), Passlib (bcrypt)
* **Фоновые задачи:** Telegram Bot Notifications
* **Тестирование:** Pytest + Pytest-Asyncio + HTTPX
* **Контейнеризация:** Docker & Docker Compose

---

## ⚡ Ключевые архитектурные решения

1. **Пессимистичная блокировка (`with_for_update`)**:
   Защита от двойного бронирования одного столика при одновременных запросах.
2. **Семантика REST API**:
   Использование корректных HTTP-статусов (`201 Created`, `409 Conflict`, `404 Not Found`).
3. **Кэширование списков столов в Redis** с инвалидацией при оформлении новой брони.
4. **Асинхронные миграции схемы БД** через Alembic.
5. **Автотесты на Pytest** (регистрация/логин, просмотр столов, валидация бронирований).

---

## 🧪 Запуск автотестов

Запуск тестов:

```text
pytest -v
```

Текущий статус прохождения:

```text
tests/test_auth.py::test_register_and_login_flow PASSED
tests/test_bookings.py::test_bookingsunauthorized PASSED
tests/test_tables.py::test_get_tables_list PASSED
====== 3 passed in 0.72s ======
```

---

## 🛠️ Локальный запуск

1. Склонировать репозиторий и перейти в папку проекта:
   ```text
   git clone <URL_РЕПОЗИТОРИЯ>
   cd project1
   ```

2. Создать и активировать виртуальное окружение:
   ```text
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. Применить миграции базы данных:
   ```text
   alembic upgrade head
   ```

4. Запустить сервер разработки:
   ```text
   uvicorn app.main:app --reload --port 8000
   ```

Интерактивная документация Swagger доступна по адресу:
`http://127.0.0.1:8000/docs`

---

## 🐳 Запуск в Docker

Для сборки и запуска контейнеров:

```text
docker-compose up --build
```