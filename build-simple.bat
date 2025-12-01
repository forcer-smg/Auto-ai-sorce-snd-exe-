@echo off
echo ========================================
echo SIMPLE BUILD - PRODUCTION SOFTWARE
echo ========================================
echo.

cd /d "C:\Users\Administrator\Auto_Punch IDE"

echo [1/4] Checking Node.js...
where node >nul 2>&1
if errorlevel 1 (
    echo   ERROR: Node.js not found!
    echo   Please install Node.js first.
    pause
    exit /b 1
)
node --version
npm --version
echo   Node.js ready.
echo.

echo [2/4] Cleaning old builds...
if exist "dist" (
    rmdir /s /q "dist" >nul 2>&1
    echo   Cleaned
) else (
    echo   No old builds
)
echo.

echo [3/4] Building installer...
echo   This will take 10-15 minutes...
echo.
call npm run build:exe

if errorlevel 1 (
    echo.
    echo   ERROR: Build failed!
    pause
    exit /b 1
)

echo.
echo [4/4] Build Complete!
echo.

if exist "dist\Auto_Punch IDE Setup 1.0.0.exe" (
    echo ========================================
    echo BUILD SUCCESSFUL!
    echo ========================================
    echo.
    echo Installer created:
    echo   dist\Auto_Punch IDE Setup 1.0.0.exe
    echo.
    echo Opening dist folder...
    start explorer dist
) else (
    echo   ERROR: Installer not found!
)

echo.
pause


