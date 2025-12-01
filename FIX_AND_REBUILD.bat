@echo off
echo ============================================================
echo   FIXING TOOLS ^& REBUILDING APPLICATION
echo ============================================================
echo.

echo [~] Stopping running processes...
taskkill /F /IM "Auto_Punch IDE.exe" >nul 2>&1
taskkill /F /FI "WINDOWTITLE eq *Flask*" /IM python.exe >nul 2>&1
timeout /t 2 /nobreak >nul

cd /d "C:\Users\Administrator\Auto_Punch IDE"

echo.
echo [~] Installing 365-Stealer dependencies...
if exist "RedTeam-Tools\365-Stealer\requirements.txt" (
    python -m pip install -q -r "RedTeam-Tools\365-Stealer\requirements.txt"
)

echo.
echo [~] Installing requests-ip-rotator...
cd "RedTeam-Tools\requests-ip-rotator"
if exist "setup.py" (
    python -m pip install -q -e .
) else (
    python -m pip install -q requests boto3
)
cd ..\..

echo.
echo [~] Building application...
call npm run build:exe

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ============================================================
    echo   BUILD SUCCESSFUL!
    echo ============================================================
    echo.
    echo All fixes applied:
    echo   - Toolkit frontend error fixed
    echo   - Tool dependencies installed
    echo   - CSS 404 errors fixed
    echo.
    echo Test with: .\TEST_BUILD.ps1
) else (
    echo.
    echo ============================================================
    echo   BUILD FAILED
    echo ============================================================
)

echo.
pause

