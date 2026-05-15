# Инструкция перед сдачей (лабораторная 12, 10 заданий)

Актуально для текущей версии проекта. **Скриншоты PR, React и OpenAI в Actions не требуются** — задание 4 это Docker + PostgreSQL.

## 1. Проверки

```powershell
cd backend
.\.venv\Scripts\activate
pytest --cov=app --cov-report=term-missing
```

```powershell
python scripts\test_room_code_regex.py
```

```powershell
docker compose up --build
```

## 2. Файлы для проверяющего

- [README.md](../README.md) — описание и API  
- [PROMPT_LOG.md](../PROMPT_LOG.md) — промпты по заданиям 1–10  
- [lab_report.md](lab_report.md) — таблица заданий  

## 3. Git

Не коммитить: `backend\.venv`, `__pycache__`, `hotel.db`, `htmlcov`.

```powershell
git add .
git commit -m "docs: lab 12 hotel API assignments 1-10"
git push
```
