@echo off
title Auto_Punch IDE - Full Server
cd /d "%~dp0"

echo ======================================
echo   Auto_Punch IDE - Full Server
echo   (With ALL API routes)
echo ======================================
echo.

echo [~] Stopping any existing servers...
taskkill /F /IM python.exe 2>nul
timeout /t 2 /nobreak >nul

echo [~] Installing dependencies...
python -m pip install -q flask flask-cors flask-socketio python-socketio
if %errorlevel% neq 0 (
    echo [!] Failed to install dependencies
    echo [!] Trying to continue anyway...
)

echo.
echo [+] Starting FULL server with all API routes...
echo [+] This is app.py (NOT simple_server.py)
echo [+] All API endpoints will be available
echo.
echo ======================================
echo   Server starting on http://localhost:5001
echo   Watch this window for request logs
echo ======================================
echo.

python app.py

pause

