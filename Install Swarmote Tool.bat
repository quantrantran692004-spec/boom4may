@echo off
setlocal
cd /d "%~dp0"

set "PYTHON_CMD="
where py >nul 2>nul
if not errorlevel 1 (
    py -3 -c "import sys; raise SystemExit(0 if sys.version_info >= (3,11) else 1)" >nul 2>nul
    if not errorlevel 1 set "PYTHON_CMD=py -3"
)

if not defined PYTHON_CMD (
    where python >nul 2>nul
    if not errorlevel 1 (
        python -c "import sys; raise SystemExit(0 if sys.version_info >= (3,11) else 1)" >nul 2>nul
        if not errorlevel 1 set "PYTHON_CMD=python"
    )
)

if not defined PYTHON_CMD (
    echo Python 3.11 or newer is required.
    choice /c YN /m "Open the official Python download page"
    if errorlevel 2 goto missing_python
    start "" "https://www.python.org/downloads/windows/"
    echo Install Python 3.11 or newer, enable Add Python to PATH, then run this file again.
    pause
    exit /b 1
)

%PYTHON_CMD% "%~dp0setup_windows.py"
set "RESULT=%ERRORLEVEL%"
if not "%RESULT%"=="0" pause
exit /b %RESULT%

:missing_python
echo Install Python 3.11 or newer, then run this file again.
pause
exit /b 1
