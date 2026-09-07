@echo off
title My Music Clone - Local Server
echo ====================================================
echo Starting My Music Clone Local Development Server...
echo ====================================================
echo.

:: 1. Check if virtual environment exists
if exist "music_project_env\Scripts\python.exe" (
    set "PYTHON_EXEC=music_project_env\Scripts\python.exe"
    echo [OK] Found virtual environment: music_project_env
) else if exist "venv\Scripts\python.exe" (
    set "PYTHON_EXEC=venv\Scripts\python.exe"
    echo [OK] Found virtual environment: venv
) else (
    set "PYTHON_EXEC=python"
    echo [WARN] Virtual environment folder not found, using global python.
)

echo.
echo [1/3] Checking database migrations...
"%PYTHON_EXEC%" manage.py migrate --noinput
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Migration failed. Please check your database settings.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo [2/3] Checking Django configuration...
"%PYTHON_EXEC%" manage.py check
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Django system check failed.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo [3/3] Launching server on http://127.0.0.1:8000
echo Open your browser and navigate to: http://127.0.0.1:8000
echo Press CTRL+C to stop the server at any time.
echo.

start "" "http://127.0.0.1:8000"
"%PYTHON_EXEC%" manage.py runserver 127.0.0.1:8000

pause
