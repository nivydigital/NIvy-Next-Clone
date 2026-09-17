@echo off
cd /d "%~dp0"
git pull
if errorlevel 1 exit /b 1
docker compose pull
docker compose up -d --build
