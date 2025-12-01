@echo off
REM ============================================================
REM TEST BUILD - Run the built executable
REM ============================================================

echo.
echo ============================================================
echo   TESTING BUILT EXECUTABLE
echo ============================================================
echo.

cd /d "%~dp0"

REM Check if executable exists
if not exist "dist\win-unpacked\Auto_Punch IDE.exe" (
    echo ERROR: Built executable not found!
    echo Expected: dist\win-unpacked\Auto_Punch IDE.exe
    echo.
    echo Please run the build first:
    echo   npm run build:exe
    echo.
    pause
    exit /b 1
)

echo [+] Found executable: dist\win-unpacked\Auto_Punch IDE.exe
echo.
echo [~] Starting Auto_Punch IDE...
echo.

REM Run the executable
start "" "dist\win-unpacked\Auto_Punch IDE.exe"

echo [+] Application started!
echo.
echo The IDE should open in a new window.
echo If it doesn't start, check:
echo   1. Python is installed and in PATH
echo   2. Flask dependencies are installed
echo   3. Port 5001 is available
echo.
pause

