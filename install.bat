@echo off
setlocal
cd /d "%~dp0"
if not exist .env copy .env.example .env
where docker >nul 2>&1 || (echo Docker is required. & exit /b 1)
echo Starting Nivy Next AIOS...
docker compose up -d --build
if errorlevel 1 exit /b 1
echo.
echo Nivy UI: http://localhost:3000
echo Nivy API: http://localhost:8000/health
echo n8n:      http://localhost:5678
echo Ollama:   http://localhost:11434
