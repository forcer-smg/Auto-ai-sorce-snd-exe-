@echo off
echo ========================================
echo STARTING FLASK SERVER
echo ========================================
echo.

cd /d "C:\Users\Administrator\Auto_Punch IDE"

echo Checking Python...
python --version
if errorlevel 1 (
    echo ERROR: Python not found!
    pause
    exit /b 1
)

echo.
echo Starting Flask server on http://localhost:5001
echo Press Ctrl+C to stop
echo.

python app.py

pause


