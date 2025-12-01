@echo off
setlocal enabledelayedexpansion
echo ========================================
echo ROBUST BUILD - AUTO RETRY AND FIX
echo ========================================
echo.

cd /d "%~dp0"

set "MAX_RETRIES=3"
set "RETRY_COUNT=0"
set "BUILD_SUCCESS=0"

:BUILD_LOOP
set /a RETRY_COUNT+=1
echo.
echo ========================================
echo BUILD ATTEMPT !RETRY_COUNT! of !MAX_RETRIES!
echo ========================================
echo.

REM Find Node.js
set "NODE_EXE="
set "NPM_EXE="
set "NODE_FOUND=0"

where node >nul 2>&1
if %errorlevel% equ 0 (
    set "NODE_EXE=node"
    set "NPM_EXE=npm"
    set "NODE_FOUND=1"
    echo [OK] Node.js found in PATH
)

if !NODE_FOUND! equ 0 (
    if exist "C:\Program Files\nodejs\node.exe" (
        set "NODE_EXE=C:\Program Files\nodejs\node.exe"
        set "NPM_EXE=C:\Program Files\nodejs\npm.cmd"
        set "PATH=%PATH%;C:\Program Files\nodejs"
        set "NODE_FOUND=1"
        echo [OK] Node.js found in Program Files
    )
)

if !NODE_FOUND! equ 0 (
    echo [ERROR] Node.js not found!
    echo Please install Node.js first.
    pause
    exit /b 1
)

REM Verify Node.js works
"%NODE_EXE%" --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js found but not working!
    pause
    exit /b 1
)

echo [OK] Node.js: 
"%NODE_EXE%" --version
echo.

REM Clean if retrying
if !RETRY_COUNT! gtr 1 (
    echo [CLEAN] Cleaning previous build attempt...
    if exist "dist" (
        rmdir /s /q "dist" >nul 2>&1
        echo [OK] Cleaned dist folder
    )
    if exist "node_modules\.cache" (
        rmdir /s /q "node_modules\.cache" >nul 2>&1
        echo [OK] Cleaned cache
    )
    timeout /t 2 /nobreak >nul
)

REM Check dependencies
echo [CHECK] Verifying dependencies...
if not exist "node_modules\electron" (
    echo [FIX] Installing dependencies...
    call "%NPM_EXE%" install
    if errorlevel 1 (
        echo [WARN] Installation had issues, but continuing...
    ) else (
        echo [OK] Dependencies installed
    )
) else (
    echo [OK] Dependencies ready
)
echo.

REM Build
echo [BUILD] Building installer...
echo This will take 10-15 minutes...
echo.

call "%NPM_EXE%" run build:exe
set "BUILD_EXIT=%errorlevel%"

if !BUILD_EXIT! equ 0 (
    echo.
    echo [CHECK] Verifying build output...
    if exist "dist\Auto_Punch IDE Setup 1.0.0.exe" (
        echo [SUCCESS] Build completed successfully!
        set "BUILD_SUCCESS=1"
    ) else (
        echo [WARN] Build reported success but installer not found
        set "BUILD_SUCCESS=0"
    )
) else (
    echo.
    echo [ERROR] Build failed with exit code !BUILD_EXIT!
    set "BUILD_SUCCESS=0"
)

REM Check result
if !BUILD_SUCCESS! equ 1 (
    echo.
    echo ========================================
    echo BUILD SUCCESSFUL!
    echo ========================================
    echo.
    for %%F in ("dist\Auto_Punch IDE Setup 1.0.0.exe") do (
        echo Installer: %%F
        echo Size: %%~zF bytes
    )
    echo.
    echo Opening dist folder...
    start explorer dist
    goto END_SUCCESS
)

REM Retry logic
if !RETRY_COUNT! lss !MAX_RETRIES! (
    echo.
    echo [RETRY] Build failed, retrying in 5 seconds...
    echo Attempt !RETRY_COUNT! of !MAX_RETRIES!
    timeout /t 5 /nobreak >nul
    goto BUILD_LOOP
) else (
    echo.
    echo ========================================
    echo BUILD FAILED AFTER !MAX_RETRIES! ATTEMPTS
    echo ========================================
    echo.
    echo Troubleshooting:
    echo   1. Check Node.js is installed correctly
    echo   2. Check disk space (need ~2 GB free)
    echo   3. Check internet connection (for downloads)
    echo   4. Try manual build: npm run build:exe
    echo.
    pause
    exit /b 1
)

:END_SUCCESS
echo.
echo Build complete! Installer ready for distribution.
echo.
pause


