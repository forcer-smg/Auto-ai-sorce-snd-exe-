@echo off
echo ========================================
echo FORCE CLEANUP - CRASHED APPS
echo ========================================
echo.

cd /d "C:\Users\Administrator\Auto_Punch IDE"

echo [1/4] Stopping all processes...
taskkill /F /IM "Auto_Punch IDE.exe" >nul 2>&1
taskkill /F /IM "AutoPunch IDE.exe" >nul 2>&1
taskkill /F /IM "autopunch.exe" >nul 2>&1

REM Find and kill Electron processes with Auto_Punch in path
for /f "tokens=2" %%p in ('tasklist /FI "IMAGENAME eq electron.exe" /FO LIST ^| findstr /I "PID"') do (
    wmic process where "ProcessId=%%p" get ExecutablePath | findstr /I "Auto_Punch" >nul
    if not errorlevel 1 (
        taskkill /F /PID %%p >nul 2>&1
        echo   Killed process PID: %%p
    )
)

timeout /t 2 /nobreak >nul
echo   Processes stopped.
echo.

echo [2/4] Finding installed locations...
if exist "%ProgramFiles%\Auto_Punch IDE" (
    echo   Found: %ProgramFiles%\Auto_Punch IDE
)
if exist "%ProgramFiles(x86)%\Auto_Punch IDE" (
    echo   Found: %ProgramFiles(x86)%\Auto_Punch IDE
)
if exist "%LOCALAPPDATA%\Programs\Auto_Punch IDE" (
    echo   Found: %LOCALAPPDATA%\Programs\Auto_Punch IDE
)
echo.

echo [3/4] Checking for uninstaller...
if exist "%ProgramFiles%\Auto_Punch IDE\uninstall.exe" (
    echo   Found uninstaller: %ProgramFiles%\Auto_Punch IDE\uninstall.exe
    echo   Run this to uninstall properly
)
if exist "%LOCALAPPDATA%\Programs\Auto_Punch IDE\uninstall.exe" (
    echo   Found uninstaller: %LOCALAPPDATA%\Programs\Auto_Punch IDE\uninstall.exe
    echo   Run this to uninstall properly
)
echo.

echo [4/4] Cleanup Summary
echo.
echo ========================================
echo CLEANUP COMPLETE
echo ========================================
echo.
echo Next steps:
echo   1. If uninstaller found, run it
echo   2. Or manually delete installed folders
echo   3. Then reinstall: .\run-installer.ps1
echo.
pause


