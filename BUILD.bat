@echo off
REM Simple Build Script - Works from Anywhere
REM Just double-click this file!

cd /d "%~dp0"

echo ========================================
echo BUILDING AUTO_PUNCH IDE
echo ========================================
echo.

echo Current directory:
cd
echo.

echo [1/3] Finding Node.js...
set "NODE_EXE="
set "NPM_EXE="

where node >nul 2>&1
if %errorlevel% equ 0 (
    set "NODE_EXE=node"
    set "NPM_EXE=npm"
    echo   Node.js found in PATH
) else (
    if exist "C:\Program Files\nodejs\node.exe" (
        set "NODE_EXE=C:\Program Files\nodejs\node.exe"
        set "NPM_EXE=C:\Program Files\nodejs\npm.cmd"
        set "PATH=%PATH%;C:\Program Files\nodejs"
        echo   Found Node.js in Program Files
    ) else (
        echo   ERROR: Node.js not found!
        echo   Please install Node.js first.
        pause
        exit /b 1
    )
)

"%NODE_EXE%" --version
"%NPM_EXE%" --version
echo.

echo [2/3] Building installer...
echo   This will take 10-15 minutes...
echo.
call "%NPM_EXE%" run build:exe

if %errorlevel% neq 0 (
    echo.
    echo   ERROR: Build failed!
    pause
    exit /b 1
)

echo.
echo [3/3] Build Complete!
echo.

if exist "dist\Auto_Punch IDE Setup 1.0.0.exe" (
    echo ========================================
    echo SUCCESS!
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


