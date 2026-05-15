# Система управления гостиницей

**ФИО:** Авдошина Ангелина Евгеньевна  
**Группа:** 221331 
**Сложность:** Средняя 
**Предметная область:** номера, бронирование, проживание, уборка, отчёты  
**Лабораторная работа:** 12 — 10 заданий с использованием ИИ  

REST API на **FastAPI** + **SQLAlchemy** + **Alembic**. Основная сущность лабораторной — **номер отеля** (эндпоинты `/items`).

Журнал промптов: [PROMPT_LOG.md](PROMPT_LOG.md)  
Сводная таблица заданий: [docs/lab_report.md](docs/lab_report.md)

---

## Выполненные задания (1–10)

| № | Задание | Реализация в проекте |
|---|---------|----------------------|
| **1** | CRUD FastAPI, Pydantic, `/items` | `backend/app/routers/items.py`, `schemas/item.py` |
| **2** | pytest, граничные случаи, ≥70% покрытия | `backend/tests/test_items_crud.py` и др. |
| **3** | Рефакторинг «плохого» кода | `legacy_bad.py` → `services/pricing.py`, [docs/assignment03_refactoring.md](docs/assignment03_refactoring.md) |
| **4** | Dockerfile + docker-compose + PostgreSQL | `docker-compose.yml`, `backend/Dockerfile` |
| **5** | Объяснение бизнес-логики | `services/pricing.py`, `services/room_score.py`, [docs/assignment05_code_explanation.md](docs/assignment05_code_explanation.md) |
| **6** | Документация README | этот файл |
| **7** | Миграции Alembic, связи, индексы | `backend/alembic/versions/001_initial_schema.py` |
| **8** | Поиск уязвимостей и исправления | [docs/assignment08_security_report.md](docs/assignment08_security_report.md), `security_api.py` |
| **9** | Аналитический SQL-запрос | [sql/top_rooms_by_revenue.sql](sql/top_rooms_by_revenue.sql), [docs/assignment09_sql_report.md](docs/assignment09_sql_report.md) |
| **10** | Regex + тестовый скрипт | [docs/task_10_regex.md](docs/task_10_regex.md), [scripts/test_room_code_regex.py](scripts/test_room_code_regex.py) |

Дополнительно (не входит в обязательные 10 заданий, но отражает предметную область): JWT-API для бронирований, гостей, уборки и отчётов — префикс `/api/*`.

---

## Установка и запуск

### Локально (SQLite)

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy ..\.env.example .env
alembic upgrade head
uvicorn app.main:app --reload --port 8000
```

- Swagger: http://127.0.0.1:8000/docs  
- Проверка: http://127.0.0.1:8000/health  

### Docker (задание 4)

```bash
docker compose up --build
```

При старте контейнера `api` выполняется `alembic upgrade head`, затем поднимается API на http://localhost:8000.

---

## Переменные окружения

| Переменная | По умолчанию | Назначение |
|------------|--------------|------------|
| `DATABASE_URL` | `sqlite:///./hotel.db` | Подключение к БД |
| `SECRET_KEY` | см. `.env.example` | JWT для `/api/*` |
| `API_KEY` | `change-me-for-local-dev` | Заголовок `X-API-Key` для POST/PUT/DELETE `/items` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `60` | Время жизни JWT |

Пример файла: [.env.example](.env.example)

---

## API `/items` (задание 1)

Модель **номера** (поля): `number`, `room_type`, `price_per_night`, `capacity`, `floor`, `description`, `status`.

| Метод | URL | API-ключ |
|-------|-----|----------|
| GET | `/items` | нет |
| POST | `/items` | да |
| GET | `/items/{id}` | нет |
| PUT | `/items/{id}` | да |
| DELETE | `/items/{id}` | да |

### Пример: создать номер

**Запрос**

```http
POST /items
Content-Type: application/json
X-API-Key: change-me-for-local-dev

{
  "number": "AB-3-12",
  "room_type": "standard",
  "price_per_night": 4500,
  "capacity": 2,
  "floor": 3,
  "description": "Вид на двор",
  "status": "available"
}
```

**Ответ** `201`

```json
{
  "id": 1,
  "number": "AB-3-12",
  "room_type": "standard",
  "price_per_night": 4500,
  "capacity": 2,
  "floor": 3,
  "description": "Вид на двор",
  "status": "available",
  "attractiveness_score": 72
}
```

### Примеры ошибок

- `404` — номер с таким `id` не найден  
- `409` — дубликат кода номера или удаление номера с бронированиями  
- `422` — невалидные данные (цена ≤ 0, неверный формат кода)  
- `401` — нет или неверный `X-API-Key` при записи  

Код номера (задание 10): `^[A-Z]{1,2}-\d{1,2}-\d{2,3}$`, например `AB-3-12`.

---

## Тесты (задание 2)

```bash
cd backend
pytest --cov=app --cov-report=term-missing
```

Покрываются: CRUD `/items`, несуществующий id, невалидные данные, API-ключ, расчёт `attractiveness_score`.

---

## Скрипт regex (задание 10)

```bash
python scripts/test_room_code_regex.py
```

---

## Миграции (задание 7)

```bash
cd backend
alembic upgrade head
```

Таблицы: `rooms`, `guests`, `bookings`, `stays`, `cleaning_tasks`, `users`. Связи: бронирование → номер и гость; проживание → бронирование; уборка → номер.

---

## Структура проекта

```
backend/app/routers/items.py   # задание 1
backend/app/legacy_bad.py      # задание 3 (до рефакторинга)
backend/app/services/          # задания 3, 5
backend/tests/                 # задание 2
backend/alembic/               # задание 7
docker-compose.yml             # задание 4
docs/                          # отчёты 3, 5, 8, 9, lab_report
sql/                           # задание 9
scripts/                       # задание 10
PROMPT_LOG.md                  # промпты ИИ по всем заданиям
```

---

## Чеклист перед сдачей

1. `cd backend && pytest` — все тесты зелёные  
2. `python scripts/test_room_code_regex.py` — без ошибок  
3. API открывается: `/docs`, `/health`  
4. В git нет `.venv`, `__pycache__`, `*.db`  
5. [PROMPT_LOG.md](PROMPT_LOG.md) заполнен  
