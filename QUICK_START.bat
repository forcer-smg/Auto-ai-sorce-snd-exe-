@echo off
title Auto_Punch IDE - Quick Start
cd /d "%~dp0"

echo ======================================
echo   Auto_Punch IDE - Quick Start
echo ======================================
echo.

echo [~] Checking Python...
python --version >nul 2>nul
if %errorlevel% neq 0 (
    echo [!] Python not found in PATH!
    echo [!] Please add Python to your PATH or use full path
    pause
    exit /b 1
)

echo [+] Python found
echo.

echo [~] Installing dependencies (if needed)...
python -m pip install --quiet flask flask-cors flask-socketio python-socketio 2>nul
echo [+] Dependencies ready
echo.

echo [+] Starting Auto_Punch IDE...
echo [+] Server: http://localhost:5001
echo [+] Press Ctrl+C to stop
echo.

python app.py

pause

