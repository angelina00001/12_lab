# Запуск API гостиницы (порт 8000)
$ErrorActionPreference = "Stop"
Set-Location "$PSScriptRoot\..\backend"

if (-not (Test-Path ".venv")) {
    Write-Host "Создаю venv..."
    py -3.12 -m venv .venv 2>$null
    if (-not $?) { python -m venv .venv }
}

.\.venv\Scripts\Activate.ps1
python -m pip install -q -r requirements-py312.txt 2>$null
if (-not $?) { pip install -r requirements.txt }

$env:SECRET_KEY = "dev-secret-key"
$env:DATABASE_URL = "sqlite:///./hotel.db"

Write-Host "API: http://127.0.0.1:8000  (документация: /docs)"
Write-Host "Логин: admin@hotel.example.com / admin123"
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
