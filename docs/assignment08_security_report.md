# Задание 8. Отчёт по безопасности (code review)

## Найденные риски

| # | Уязвимость | Где | Риск |
|---|------------|-----|------|
| 1 | Слабый `SECRET_KEY` по умолчанию | `config.py` | Подделка JWT |
| 2 | CORS `allow_origins=["*"]` при расширении | `main.py` | CSRF с чужих сайтов |
| 3 | Слабый API-ключ по умолчанию | `config.py` | Подделка write-запросов при утечке ключа |
| 4 | Отсутствие security-заголовков | middleware | XSS/clickjacking |
| 5 | Пароли в seed для демо | `seed.py` | Утечка в проде |

## SQL-инъекции

Используется SQLAlchemy ORM и параметризованные запросы — **raw SQL с конкатенацией не применяется**. Риск низкий.

## XSS

API возвращает JSON; HTML-дашборд не встроен в CRUD. Заголовок `X-Content-Type-Options: nosniff` добавлен.

## Валидация входа

- Pydantic на `/items` (цена, вместимость, **regex кода номера**).
- Ограничения длины строк в схемах.

## Исправления (внесены)

1. `SecurityHeadersMiddleware` — `X-Frame-Options`, `X-XSS-Protection`, `Referrer-Policy`.
2. Документировано: в production задать `SECRET_KEY` через env (см. `.env.example`).
3. Для `/items` write-операции защищены заголовком **`X-API-Key`**; read — без ключа. Расширенное API `/api/*` — JWT.
4. Рекомендация в README: не использовать demo-пароли в production.

## Рекомендации на будущее

- Rate limiting (slowapi)
- HTTPS-only cookies при cookie-auth
- RBAC на `/items` в production
- Регулярный `pip audit` / Dependabot
