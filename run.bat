@echo off
title Auto_Punch IDE
cd /d "%~dp0"

echo ======================================
echo   Auto_Punch IDE - VS Code + Cursor Clone
echo   Powered by Auto_Punch Ai
echo ======================================
echo.

echo [~] Checking for Python...
python --version >nul 2>nul
if %errorlevel% neq 0 (
    echo [!] Python is not installed or not in PATH.
    echo [!] Please install Python from https://www.python.org/downloads/
    pause
    exit /b 1
)
echo [+] Python found.
echo.

echo [~] Installing dependencies...
python -m pip install -q -r requirements.txt
if %errorlevel% neq 0 (
    echo [!] Error installing dependencies.
    pause
    exit /b 1
)
echo [+] Dependencies installed.
echo.

echo [+] Starting Auto_Punch IDE...
echo [+] The IDE will open in your browser automatically.
echo [+] If it doesn't open, go to: http://localhost:5001
echo.

python app.py

pause

