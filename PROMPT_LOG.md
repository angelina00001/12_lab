# PROMPT_LOG — журнал промптов к ИИ

**Студент:** Авдошина Ангелина Евгеньевна, группа 221331  
**Тема:** Система управления гостиницей (номера, бронирование, проживание, уборка, отчёты)  
**Инструмент:** Cursor AI  
**Стек:** Python, FastAPI, SQLAlchemy, Alembic, pytest, Docker, PostgreSQL  

---

## Задание 1. Генерация CRUD-приложения

### Промпт

```
Сгенерируй REST API на FastAPI для предметной области «гостиница».
Основная сущность — номер отеля (hotel room).

Требования:
- не менее 5 полей в модели (код номера, тип, цена за ночь, вместимость, этаж, описание, статус);
- эндпоинты: GET /items, POST /items, GET /items/{id}, PUT /items/{id}, DELETE /items/{id};
- валидация через Pydantic (цена > 0, длины строк);
- обработка ошибок 404, 409, 422;
- type hints везде;
- код должен запускаться через uvicorn.
```

### Результат

Файлы `backend/app/routers/items.py`, `backend/app/schemas/item.py`.  
Модель SQLAlchemy `Room` в `models/room.py`.

### Замечания

ИИ сначала предложил только `/api/rooms` с JWT. Добавлен отдельный роутер `/items` по формулировке задания.  
Для записи (POST/PUT/DELETE) позже добавлен заголовок `X-API-Key` (задание 8).

---

## Задание 2. Генерация тестов

### Промпт

```
Напиши модульные тесты pytest для CRUD /items гостиницы.

Нужно покрыть:
- создание, чтение списка, чтение по id, обновление, удаление;
- 404 для несуществующего id;
- 422 для невалидных данных (отрицательная цена, неверный код номера);
- 409 при дубликате кода номера;
- проверку заголовка X-API-Key на write-операциях.

Используй TestClient, in-memory SQLite, fixtures client и db.
Цель — покрытие ключевых маршрутов не менее 70%.
```

### Результат

`backend/tests/test_items_crud.py`, `tests/conftest.py`, `tests/test_room_score.py`.  
Прогон: `pytest --cov=app` — покрытие около 85%, все тесты passed.

### Замечания

После обновления `conftest.py` пришлось восстановить fixtures `auth_header`, `admin_token` для тестов расширенного `/api/*`.

---

## Задание 3. Рефакторинг «плохого» кода

### Промпт (создание плохого кода)

```
Напиши намеренно плохую функцию на Python для расчёта стоимости проживания в отеле:
длина больше 30 строк, магические числа 0.9, 500, 0.15,
непонятные имена параметров x, y, z, a, b…,
дублирование if-блоков, без проверки дат и без docstring.
```

### Промпт (рефакторинг)

```
Отрефактори эту функцию для гостиницы: понятные имена, константы,
проверка дат заезда/выезда, dataclass результата, без дублирования.
Объясни каждое изменение в отдельном markdown-файле для отчёта.
```

### Результат

- До: `backend/app/legacy_bad.py` — функция `calc(...)`  
- После: `backend/app/services/pricing.py`, `stay_charges.py`  
- Отчёт: `docs/assignment03_refactoring.md`

---

## Задание 4. Генерация Docker-конфигурации

### Промпт

```
Создай Dockerfile для FastAPI-приложения в папке backend и docker-compose.yml:
- сервис PostgreSQL;
- сервис api с переменными DATABASE_URL и SECRET_KEY;
- при старте api выполнить alembic upgrade head, затем uvicorn;
- учесть .env.example для локальной разработки.
```

### Результат

`backend/Dockerfile`, `docker-compose.yml` (сервисы `db`, `api`).

### Замечания

Локально без Docker используется SQLite; в compose — PostgreSQL.

---

## Задание 5. Объяснение сложного кода

### Промпт

```
В проекте гостиницы есть бизнес-логика:
1) calculate_stay_price — скидки за длительное проживание, штраф за поздний выезд, наценка в сезон;
2) calculate_room_attractiveness_score — индекс привлекательности номера 0–100.

Объясни простым языком, как работают обе функции, приведи числовой пример.
Предложи улучшения (Decimal, вынос тарифов в конфиг).
Сохрани объяснение в docs/assignment05_code_explanation.md.
```

### Результат

`backend/app/services/pricing.py`, `room_score.py`, документ `docs/assignment05_code_explanation.md`.  
В ответе API `/items` поле `attractiveness_score` считается автоматически.

---

## Задание 6. Генерация документации

### Промпт

```
Напиши полный README.md для лабораторной «Система управления гостиницей»:
ФИО Авдошина Ангелина Евгеньевна, группа 221331;
таблица всех 10 заданий с путями к файлам;
установка локально и через Docker;
описание /items с примерами запроса и ответа;
переменные окружения;
команды pytest и regex-скрипта;
чеклист перед сдачей.
Без упоминания Go, React, скриншотов PR и старых заданий.
```

### Результат

Файл `README.md` (корень репозитория).

---

## Задание 7. Генерация миграций БД

### Промпт

```
Сгенерируй Alembic-миграцию для гостиницы:
таблицы users, rooms, guests, bookings, stays, cleaning_tasks;
связи bookings.room_id -> rooms, bookings.guest_id -> guests,
stays.booking_id -> bookings, cleaning_tasks.room_id -> rooms;
индексы на room.number, bookings.check_in, bookings.status, cleaning_tasks.status.
```

### Результат

`backend/alembic/env.py`, `alembic/versions/001_initial_schema.py`.

---

## Задание 8. Поиск уязвимостей в коде

### Промпт

```
Проведи code review FastAPI-приложения гостиницы как security reviewer.
Найди: SQL-инъекции, XSS, незащищённые эндпоинты, слабый SECRET_KEY, отсутствие валидации.
Дай отчёт в markdown и исправь код:
- API-ключ X-API-Key для POST/PUT/DELETE /items;
- security headers middleware;
- запрет HTML в description;
- централизованные exception handlers.
```

### Результат

`docs/assignment08_security_report.md`, `app/security_api.py`, `app/exceptions.py`, `middleware/security.py`.

---

## Задание 9. Генерация SQL-запросов

### Промпт

```
Сформулируй на русском аналитический отчёт для гостиницы:
«Топ-10 номеров по суммарной выручке от бронирований за последние 30 дней
с количеством бронирований».

Напиши SQL для PostgreSQL с LEFT JOIN, GROUP BY, ORDER BY, LIMIT.
Объясни логику запроса в отдельном markdown.
```

### Результат

`sql/top_rooms_by_revenue.sql`, `docs/assignment09_sql_report.md`.

---

## Задание 10. Генерация регулярного выражения

### Промпт

```
Для гостиницы нужна валидация инвентарного кода номера:
формат КОРПУС-ЭТАЖ-НОМЕР, например AB-3-12 или A-1-05.
Сгенерируй regex, добавь в Pydantic-схему ItemCreate,
напиши скрипт scripts/test_room_code_regex.py с валидными и невалидными примерами
и краткую документацию docs/task_10_regex.md.
```

### Результат

Паттерн `^[A-Z]{1,2}-\d{1,2}-\d{2,3}$` в `schemas/item.py`, скрипт `scripts/test_room_code_regex.py`, документ `docs/task_10_regex.md`.

---

## Сводная таблица

| № | Промпт (кратко) | Основные файлы |
|---|-----------------|----------------|
| 1 | CRUD /items для номеров | `routers/items.py`, `schemas/item.py` |
| 2 | pytest CRUD + границы | `tests/test_items_crud.py` |
| 3 | плохой calc → pricing | `legacy_bad.py`, `services/pricing.py` |
| 4 | Docker + Postgres | `docker-compose.yml`, `Dockerfile` |
| 5 | объяснить pricing и score | `assignment05_code_explanation.md` |
| 6 | README | `README.md` |
| 7 | Alembic схема | `alembic/versions/001_*.py` |
| 8 | security review | `assignment08_security_report.md` |
| 9 | SQL топ номеров | `top_rooms_by_revenue.sql` |
| 10 | regex кода номера | `test_room_code_regex.py` |
