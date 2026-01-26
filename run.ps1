# PowerShell startup script for Data Management Portal

Write-Host ""
Write-Host "======================================" -ForegroundColor Cyan
Write-Host "Data Management Portal - Startup" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# Check if virtual environment exists
if (-not (Test-Path ".\.venv")) {
    Write-Host "ERROR: Virtual environment not found!" -ForegroundColor Red
    Write-Host "Please run setup first by following QUICKSTART.md" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& ".\.venv\Scripts\Activate.ps1"

Write-Host ""
Write-Host "✓ Virtual environment activated" -ForegroundColor Green
Write-Host ""

# Run migrations silently
Write-Host "Checking database..." -ForegroundColor Yellow
& python manage.py migrate --noinput 2>$null

Write-Host ""
Write-Host "======================================" -ForegroundColor Cyan
Write-Host "Starting Django Development Server" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Portal URL: http://localhost:8000/" -ForegroundColor Green
Write-Host "Admin URL:  http://localhost:8000/admin/" -ForegroundColor Green
Write-Host ""
Write-Host "Test Credentials:" -ForegroundColor Cyan
Write-Host "  Director:  director_test / Director123!" -ForegroundColor White
Write-Host "  Scientist: scientist_test / Scientist123!" -ForegroundColor White
Write-Host "  Staff:     staff_test / Staff123!" -ForegroundColor White
Write-Host ""
Write-Host "Press CTRL+C to stop the server" -ForegroundColor Yellow
Write-Host ""

& python manage.py runserver
