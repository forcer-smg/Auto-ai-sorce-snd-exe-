@echo off
echo ========================================
echo AUTO-RUN ALL - COMPLETE AUTOMATION
echo ========================================
echo.

cd /d "C:\Users\Administrator\Auto_Punch IDE"

echo [1/5] Stopping interfering processes...
taskkill /F /IM python.exe /T >nul 2>&1
taskkill /F /IM pythonw.exe /T >nul 2>&1
timeout /t 2 /nobreak >nul
echo   Done.

echo.
echo [2/5] Verifying Node.js...
set "NODE_EXE="
set "NPM_EXE="

REM Check if node is in PATH
where node >nul 2>&1
if not errorlevel 1 (
    set "NODE_EXE=node"
    set "NPM_EXE=npm"
    echo   Node.js found in PATH
) else (
    echo   Checking common Node.js locations...
    if exist "C:\Program Files\nodejs\node.exe" (
        set "NODE_EXE=C:\Program Files\nodejs\node.exe"
        set "NPM_EXE=C:\Program Files\nodejs\npm.cmd"
        set "PATH=%PATH%;C:\Program Files\nodejs"
        echo   Found Node.js in Program Files
    ) else if exist "C:\Program Files (x86)\nodejs\node.exe" (
        set "NODE_EXE=C:\Program Files (x86)\nodejs\node.exe"
        set "NPM_EXE=C:\Program Files (x86)\nodejs\npm.cmd"
        set "PATH=%PATH%;C:\Program Files (x86)\nodejs"
        echo   Found Node.js in Program Files (x86)
    ) else if exist "%LOCALAPPDATA%\Programs\nodejs\node.exe" (
        set "NODE_EXE=%LOCALAPPDATA%\Programs\nodejs\node.exe"
        set "NPM_EXE=%LOCALAPPDATA%\Programs\nodejs\npm.cmd"
        set "PATH=%PATH%;%LOCALAPPDATA%\Programs\nodejs"
        echo   Found Node.js in Local AppData
    ) else (
        echo   ERROR: Node.js not found!
        echo   Please install Node.js first or restart your terminal.
        pause
        exit /b 1
    )
)

REM Verify Node.js works
"%NODE_EXE%" --version >nul 2>&1
if errorlevel 1 (
    echo   ERROR: Node.js found but not working!
    pause
    exit /b 1
)
for /f "tokens=*" %%v in ('"%NODE_EXE%" --version') do set NODE_VERSION=%%v
for /f "tokens=*" %%v in ('"%NPM_EXE%" --version') do set NPM_VERSION=%%v
echo   Node.js: %NODE_VERSION%
echo   npm: %NPM_VERSION%
echo   Node.js ready.

echo.
echo [3/5] Checking dependencies...
if exist "node_modules\electron" (
    echo   Electron: Ready
) else (
    echo   Electron: Missing - Installing...
    call "%NPM_EXE%" install
)

echo.
echo [4/5] Checking build status...
if exist "dist\Auto_Punch IDE Setup 1.0.0.exe" (
    echo   Installer: Found
    for %%F in ("dist\Auto_Punch IDE Setup 1.0.0.exe") do (
        echo   Size: %%~zF bytes
    )
) else (
    echo   Installer: Not found - Building...
    echo   This will take 10-15 minutes...
    call "%NPM_EXE%" run build:exe
    if errorlevel 1 (
        echo   Build failed. Check errors above.
        pause
        exit /b 1
    )
)

echo.
echo [5/5] Final Summary
echo.
echo ========================================
echo ALL STEPS COMPLETE!
echo ========================================
echo.
echo Installer Location:
if exist "dist\Auto_Punch IDE Setup 1.0.0.exe" (
    echo   dist\Auto_Punch IDE Setup 1.0.0.exe
) else (
    echo   Installer not found - build may have failed
)

echo.
echo Opening dist folder...
timeout /t 1 /nobreak >nul
start explorer dist

echo.
echo ========================================
echo READY FOR NEXT STEPS!
echo ========================================
echo.
pause


