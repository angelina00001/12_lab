# Запуск UI (порт 5173) — сначала запустите start-backend.ps1 в другом окне!
Set-Location "$PSScriptRoot\..\frontend"
if (-not (Test-Path "node_modules")) { npm install }
Write-Host "UI: http://localhost:5173"
npm run dev
