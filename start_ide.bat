@echo off
title Auto_Punch IDE Server
cd /d "%~dp0"

echo ======================================
echo   Auto_Punch IDE - Starting Server
echo ======================================
echo.

echo [~] Checking Python...
python --version
if %errorlevel% neq 0 (
    echo [!] Python not found!
    pause
    exit /b 1
)

echo.
echo [~] Installing/Updating dependencies...
pip install -q flask flask-cors flask-socketio python-socketio
if %errorlevel% neq 0 (
    echo [!] Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo [+] Starting Auto_Punch IDE server...
echo [+] Server will run on: http://localhost:5001
echo [+] Press Ctrl+C to stop the server
echo.

python app.py

pause

