@echo off
echo ======================================
echo   Verifying Auto_Punch IDE Server
echo ======================================
echo.

echo [1] Checking if server is running on port 5001...
netstat -ano | findstr :5001
if %errorlevel% equ 0 (
    echo [+] Server is running!
) else (
    echo [-] Server is NOT running
    echo     Please start it with: python app.py
    pause
    exit /b 1
)

echo.
echo [2] Testing API endpoints...
echo.

echo Testing /api/workspace/get...
curl -s http://localhost:5001/api/workspace/get
echo.
echo.

echo Testing /api/debug/info...
curl -s http://localhost:5001/api/debug/info
echo.
echo.

echo ======================================
echo   Verification Complete
echo ======================================
echo.
echo If you see JSON responses above, the server is working!
echo.
echo Open your browser to:
echo   http://localhost:5001
echo.
pause

