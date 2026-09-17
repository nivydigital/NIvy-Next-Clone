@echo off
setlocal
set "ROOT=G:\Docker\Nivy\Repository\Nivy-Next-AIOS"

echo ============================================================
echo NIVY NEXT AIOS V1 - ONE CLICK FULL TEST
echo Repository : %ROOT%
echo ============================================================

if not exist "%ROOT%\setup\TEST-V1-ALL-AGENTS.ps1" (
  echo ERROR: Repository is not installed at %ROOT%.
  pause
  exit /b 1
)

powershell -NoProfile -ExecutionPolicy Bypass -File "%ROOT%\setup\TEST-V1-ALL-AGENTS.ps1" -NoDockerStart
set "RC=%ERRORLEVEL%"

echo.
if "%RC%"=="0" (
  echo V1 TEST SEQUENCE FINISHED.
) else (
  echo V1 TEST SEQUENCE RETURNED ERRORLEVEL %RC%.
)
pause
exit /b %RC%
