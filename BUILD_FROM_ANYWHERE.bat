@echo off
REM Build from Any Directory
REM This script will find the project and build it

echo ========================================
echo AUTO_PUNCH IDE - BUILD FROM ANYWHERE
echo ========================================
echo.

REM Try to find the project directory
set "PROJECT_DIR=C:\Users\Administrator\Auto_Punch IDE"

if not exist "%PROJECT_DIR%" (
    echo ERROR: Project directory not found!
    echo Expected: %PROJECT_DIR%
    pause
    exit /b 1
)

echo Changing to project directory...
cd /d "%PROJECT_DIR%"
echo Current directory: %CD%
echo.

REM Find Node.js
set "NODE_EXE="
set "NPM_EXE="

where node >nul 2>&1
if %errorlevel% equ 0 (
    set "NODE_EXE=node"
    set "NPM_EXE=npm"
) else (
    if exist "C:\Program Files\nodejs\node.exe" (
        set "NODE_EXE=C:\Program Files\nodejs\node.exe"
        set "NPM_EXE=C:\Program Files\nodejs\npm.cmd"
        set "PATH=%PATH%;C:\Program Files\nodejs"
    ) else (
        echo ERROR: Node.js not found!
        pause
        exit /b 1
    )
)

echo Node.js: 
"%NODE_EXE%" --version
echo.

echo Building installer...
echo This will take 10-15 minutes...
echo.

call "%NPM_EXE%" run build:exe

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo BUILD SUCCESSFUL!
    echo ========================================
    echo.
    if exist "dist\Auto_Punch IDE Setup 1.0.0.exe" (
        echo Installer: dist\Auto_Punch IDE Setup 1.0.0.exe
        start explorer dist
    )
) else (
    echo.
    echo BUILD FAILED!
    echo Check errors above.
)

echo.
pause


