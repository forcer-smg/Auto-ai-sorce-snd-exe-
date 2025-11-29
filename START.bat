@echo off
title Auto_Punch IDE
cd /d "%~dp0"

echo ======================================
echo   Auto_Punch IDE
echo ======================================
echo.

REM Check Python
python --version >nul 2>nul
if %errorlevel% neq 0 (
    echo [!] ERROR: Python not found!
    echo     Please install Python or add it to PATH
    pause
    exit /b 1
)

REM Try to install dependencies (silently, don't fail if already installed)
echo [~] Checking dependencies...
python -m pip install --quiet --upgrade flask flask-cors flask-socketio python-socketio 2>nul
echo [+] Ready
echo.

echo [+] Starting server...
echo [+] Open: http://localhost:5001
echo [+] Press Ctrl+C to stop
echo.

python app.py

pause

