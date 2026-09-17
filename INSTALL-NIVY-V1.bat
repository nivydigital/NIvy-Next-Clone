@echo off
setlocal EnableExtensions

REM ============================================================
REM NIVY NEXT V1 - ONE-CLICK WINDOWS INSTALL / BOOTSTRAP
REM Canonical root: G:\Docker\Nivy
REM ============================================================

set "ROOT=G:\Docker\Nivy"
set "REPO=%ROOT%\Repository\Nivy-Next-AIOS"
set "DATA=%ROOT%\Data"
set "LOGS=%ROOT%\Logs"
set "INSTALLER=%REPO%\setup\INSTALL-ALL-WINDOWS.ps1"
set "RC=1"

cd /d "%ROOT%" 2>nul
if errorlevel 1 mkdir "%ROOT%" >nul 2>&1

:START
echo.
echo ============================================================
echo NIVY NEXT AIOS V1 - ONE CLICK WINDOWS INSTALL
 echo Repository : %REPO%
echo Data       : %DATA%
echo Logs       : %LOGS%
echo ============================================================
echo.

where powershell.exe >nul 2>&1
if errorlevel 1 (
  echo [ERROR] Windows PowerShell was not found.
  goto :FAIL
)

where git >nul 2>&1
if errorlevel 1 (
  echo [ERROR] Git is not installed or not on PATH.
  echo Install Git, reopen CMD, then run this file again.
  goto :FAIL
)

REM If this launcher is being run from a copied/downloaded location,
REM bootstrap the canonical repository first. This removes the old
REM dependency on %~dp0\setup existing beside the BAT file.
if not exist "%INSTALLER%" (
  echo [1/3] Canonical repository is missing. Cloning it now...
  if exist "%REPO%" (
    echo [ERROR] %REPO% exists but setup\INSTALL-ALL-WINDOWS.ps1 is missing.
    echo Rename/remove that incomplete folder, then rerun this installer.
    goto :FAIL
  )
  mkdir "%ROOT%\Repository" >nul 2>&1
  git clone https://github.com/nivyindia/Nivy-Next-AIOS.git "%REPO%"
  if errorlevel 1 (
    echo [ERROR] Git clone failed. Check internet access and GitHub authentication.
    goto :FAIL
  )
)

if not exist "%INSTALLER%" (
  echo [ERROR] Installer script is still missing after repository bootstrap.
  goto :FAIL
)

echo [2/3] Running complete Windows V1 bootstrap...
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%INSTALLER%" -InstallRoot "%REPO%" -DataRoot "%DATA%" -LogRoot "%LOGS%"
set "RC=%ERRORLEVEL%"

echo.
if "%RC%"=="0" (
  echo ============================================================
  echo INSTALLATION AND V1 TEST SEQUENCE FINISHED.
  echo ============================================================
) else (
  echo ============================================================
  echo INSTALLATION RETURNED ERRORLEVEL %RC%.
  echo Review the PowerShell output above.
  echo ============================================================
)

echo [3/3] Repository: %REPO%
echo       Data:       %DATA%
echo       Logs:       %LOGS%
echo.
goto :END

:FAIL
echo.
echo ============================================================
echo INSTALLATION FAILED
 echo Review the error shown above.
echo ============================================================
set "RC=1"

:END
echo.
echo Press any key to close this window...
pause >nul
exit /b %RC%
