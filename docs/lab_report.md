# Лабораторная работа: Система управления гостиницей

## Тема

Предметная область: **номера, бронирование, проживание, уборка, отчёты**.

Основная CRUD-сущность (задание 1): **номер отеля** — эндпоинты `/items` (аналог `/clients` в [MetLab12](https://github.com/YukioYanagi/MetLab12)).

## Карта заданий

| Задание | Что сделано | Файлы |
| --- | --- | --- |
| 1 | FastAPI CRUD `/items`, Pydantic, ошибки | `backend/app/routers/items.py`, `schemas/item.py` |
| 2 | pytest CRUD + граничные случаи | `backend/tests/test_items_crud.py` |
| 3 | Рефакторинг плохой функции | [assignment03_refactoring.md](assignment03_refactoring.md), `legacy_bad.py`, `services/pricing.py` |
| 4 | Docker + PostgreSQL + Alembic | `docker-compose.yml`, `backend/Dockerfile` |
| 5 | Бизнес-логика (pricing + attractiveness_score) | [assignment05_code_explanation.md](assignment05_code_explanation.md), `services/room_score.py` |
| 6 | README | [README.md](../README.md) |
| 7 | Миграции, связи, индексы | `backend/alembic/versions/` |
| 8 | Security review | [assignment08_security_report.md](assignment08_security_report.md), `security_api.py` |
| 9 | SQL-отчёт | [assignment09_sql_report.md](assignment09_sql_report.md), `sql/top_rooms_by_revenue.sql` |
| 10 | Regex кода номера | [task_10_regex.md](task_10_regex.md), `scripts/test_room_code_regex.py` |

## Отличия от эталона MetLab12

| MetLab12 (CRM) | Наш проект (гостиница) |
| --- | --- |
| `/clients` | `/items` (номера; по ТЗ лабораторной) |
| `health_score` | `attractiveness_score` |
| Код `CLT-YYYY-NNNNN` | Код `AB-3-12` |
| Плоская структура `app/` в корне | `backend/app/` + расширенное `/api/*` с JWT |
| Только CRM API | + бронирования, уборка, отчёты |
