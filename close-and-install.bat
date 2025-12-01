@echo off
echo ========================================
echo CLOSING AUTO_PUNCH IDE AND INSTALLING
echo ========================================
echo.

cd /d "C:\Users\Administrator\Auto_Punch IDE"

echo [1/3] Closing Auto_Punch IDE processes...
taskkill /F /IM "Auto_Punch IDE.exe" >nul 2>&1
taskkill /F /IM "AutoPunch IDE.exe" >nul 2>&1
taskkill /F /IM "autopunch.exe" >nul 2>&1

REM Find Electron processes with Auto_Punch in path
for /f "tokens=2" %%p in ('tasklist /FI "IMAGENAME eq electron.exe" /FO LIST ^| findstr /I "PID"') do (
    wmic process where "ProcessId=%%p" get ExecutablePath | findstr /I "Auto_Punch" >nul
    if not errorlevel 1 (
        taskkill /F /PID %%p >nul 2>&1
        echo   Closed Electron process (PID: %%p)
    )
)

timeout /t 3 /nobreak >nul
echo   Processes closed.

echo.
echo [2/3] Verifying installer...
if not exist "dist\Auto_Punch IDE Setup 1.0.0.exe" (
    echo   ERROR: Installer not found!
    echo   Please build the installer first.
    pause
    exit /b 1
)
echo   Installer found.

echo.
echo [3/3] Running installer...
echo   Starting installer...
echo.
start /wait "dist\Auto_Punch IDE Setup 1.0.0.exe"

if %errorlevel% equ 0 (
    echo.
    echo   Installer completed!
) else (
    echo.
    echo   Installer may have had issues.
)

echo.
echo ========================================
echo INSTALLATION COMPLETE!
echo ========================================
echo.
pause


