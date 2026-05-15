# Чеклист перед сдачей (по заданиям курса)

## Задание 1 — веб-приложение

- [ ] Регистрация, логин, JWT (`/api/auth/*`)
- [ ] CRUD основной сущности — **номера** (`/api/rooms`)
- [ ] ≥3 связанные сущности: бронирование, гости, проживание, уборка
- [ ] Отчёты (`/api/reports/*`)
- [ ] Роли admin/staff/guest + админ-панель
- [ ] Промпты в [PROMPT_LOG.md](../PROMPT_LOG.md)
- [ ] Backend: `uvicorn app.main:app --reload`
- [ ] Frontend: `npm run dev` → http://localhost:5173

## Задание 2 — code review

- [ ] Отчёт ≥5 пунктов: [code-review-report.md](code-review-report.md)

## Задание 4 — CI/CD + AI

- [ ] Workflow PR: `.github/workflows/pr-ai-review.yml`
- [ ] Секрет `OPENAI_API_KEY` на GitHub (для AI-комментария)
- [ ] Скриншот комментария ИИ в PR: [assignment4-screenshot.md](assignment4-screenshot.md)

## Задание 7 — тесты и покрытие

- [ ] `cd backend && pytest --cov=app --cov-report=term-missing`
- [ ] Покрытие ≥90% (или зафиксировать факт в `coverage-summary.txt`)
- [ ] Промпты тестов в [PROMPT_LOG.md](../PROMPT_LOG.md) (задание 7)

## Git / репозиторий

- [ ] `git clone` в пустую папку → проект запускается
- [ ] Нет в git: `.venv`, `node_modules`, `*.db`, `htmlcov`, `__pycache__`
- [ ] `pytest` — зелёные
- [ ] README заполнен (ФИО, группа/вариант)

## Команды проверки

```bash
cd backend
python --version   # должно быть 3.12.x или 3.13.x
pip install -r requirements.txt
set SECRET_KEY=test-secret
set DATABASE_URL=sqlite://
pytest --cov=app --cov-report=term-missing --cov-fail-under=85
```

```bash
cd frontend
npm install
npm run build
```
