@echo off
REM Startup script for Data Management Portal
REM Run this file to start the Django development server

echo.
echo ======================================
echo Data Management Portal - Startup
echo ======================================
echo.

REM Check if virtual environment exists
if not exist ".venv\" (
    echo ERROR: Virtual environment not found!
    echo Please run setup first by following QUICKSTART.md
    pause
    exit /b 1
)

REM Activate virtual environment
echo Activating virtual environment...
call .\.venv\Scripts\activate.bat

if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

echo.
echo ✓ Virtual environment activated
echo.

REM Run migrations
echo Checking database...
python manage.py migrate --noinput > nul 2>&1

REM Start server
echo.
echo ======================================
echo Starting Django Development Server
echo ======================================
echo.
echo Portal URL: http://localhost:8000/
echo Admin URL:  http://localhost:8000/admin/
echo.
echo Test Credentials:
echo   Director:  director_test / Director123!
echo   Scientist: scientist_test / Scientist123!
echo   Staff:     staff_test / Staff123!
echo.
echo Press CTRL+C to stop the server
echo.

python manage.py runserver
