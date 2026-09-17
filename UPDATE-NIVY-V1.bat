@echo off
setlocal EnableExtensions

REM ============================================================
REM NIVY NEXT V1 - ONE-CLICK UPDATE
REM Canonical root: G:\Docker\Nivy
REM ============================================================

set "ROOT=G:\Docker\Nivy"
set "REPO=%ROOT%\Repository\Nivy-Next-AIOS"
set "INSTALLER=%REPO%\setup\INSTALL-ALL-WINDOWS.ps1"
set "TESTER=%REPO%\setup\TEST-V1-ALL-AGENTS.ps1"
set "RC=1"

REM Force a visible CMD session and never silently close on failure.
echo.
echo ============================================================
echo NIVY NEXT AIOS V1 - UPDATE
 echo Repository: %REPO%
echo ============================================================
echo.

REM Git is required for update.
where git.exe >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Git was not found on PATH.
    echo Install Git, restart CMD, and run this file again.
    goto :END
)

REM PowerShell is required for the installer/tester.
where powershell.exe >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Windows PowerShell was not found.
    goto :END
)

REM If the repo does not exist, bootstrap it instead of failing.
if not exist "%REPO%\.git" (
    echo [INFO] Canonical repository is missing.
    echo [INFO] Bootstrapping the repository first...
    if not exist "%ROOT%" mkdir "%ROOT%"
    if not exist "%ROOT%\Repository" mkdir "%ROOT%\Repository"
    git clone https://github.com/nivyindia/Nivy-Next-AIOS.git "%REPO%"
    if errorlevel 1 (
        echo [ERROR] Git clone failed.
        echo Check internet access and GitHub authentication/permissions.
        goto :END
    )
) else (
    cd /d "%REPO%"
    if errorlevel 1 (
        echo [ERROR] Could not enter repository directory.
        goto :END

    echo [1/4] Checking local repository...
    git status --short
    if errorlevel 1 (
        echo [ERROR] Git status failed.
        goto :END
    )

    echo.
    echo [2/4] Fetching latest main branch...
    git fetch origin
    if errorlevel 1 (
        echo [ERROR] git fetch failed.
        goto :END
    )

    git checkout main
    if errorlevel 1 (
        echo [ERROR] Could not checkout main.
        goto :END
    )

    git pull --ff-only origin main
    if errorlevel 1 (
        echo [ERROR] Fast-forward update failed.
        echo Local commits/changes were NOT overwritten.
        goto :END
    )
)

REM Refresh the expected paths after clone/pull.
if not exist "%INSTALLER%" (
    echo [ERROR] Installer script is missing:
    echo %INSTALLER%
    goto :END
)
if not exist "%TESTER%" (
    echo [ERROR] Test runner is missing:
    echo %TESTER%
    goto :END
)

if not exist "%ROOT%\Data" mkdir "%ROOT%\Data"
if not exist "%ROOT%\Logs" mkdir "%ROOT%\Logs"

cd /d "%REPO%"
if errorlevel 1 goto :END

echo.
echo [3/4] Applying latest V1 configuration...
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%INSTALLER%" -InstallRoot "%REPO%" -DataRoot "%ROOT%\Data" -LogRoot "%ROOT%\Logs" -SkipPrerequisites -SkipDockerStart -SkipTerraform -SkipTests -SkipAgentTests
set "INSTALL_RC=%ERRORLEVEL%"
if not "%INSTALL_RC%"=="0" (
    echo [ERROR] Configuration update failed with exit code %INSTALL_RC%.
    goto :END
)

echo.
echo [4/4] Running V1 verification...
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%TESTER%" -NoDockerStart
set "RC=%ERRORLEVEL%"

if "%RC%"=="0" (
    echo.
    echo ============================================================
    echo UPDATE COMPLETE - V1 VERIFICATION PASSED
    echo ============================================================
) else (
    echo.
    echo ============================================================
    echo UPDATE COMPLETED, BUT V1 VERIFICATION FAILED
    echo Exit code: %RC%
    echo Review the test output above.
    echo ============================================================
)

echo.
echo Repository: %REPO%
echo Data:       %ROOT%\Data
echo Logs:       %ROOT%\Logs

:END
echo.
echo ============================================================
echo UPDATE SCRIPT FINISHED - EXIT CODE %RC%
echo Press any key to close this window...
echo ============================================================
pause >nul
exit /b %RC%
