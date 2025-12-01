@echo off
echo ========================================
echo Auto_Punch IDE - Complete Setup
echo ========================================
echo.

cd /d "C:\Users\Administrator\Auto_Punch IDE"

echo [1/4] Verifying Node.js...
node --version
npm --version
if errorlevel 1 (
    echo Node.js not found. Please install Node.js first.
    pause
    exit /b 1
)

echo.
echo [2/4] Installing npm dependencies...
echo This will take 5-10 minutes. Please wait...
call npm install
if errorlevel 1 (
    echo Installation had issues. Trying with --force...
    call npm install --force
)

echo.
echo [3/4] Verifying installation...
if exist "node_modules\electron" (
    echo Electron: Ready
) else (
    echo Electron: Missing - installation may have failed
)

if exist "node_modules\electron-builder" (
    echo electron-builder: Ready
) else (
    echo electron-builder: Missing - installation may have failed
)

echo.
echo [4/4] Building installers...
echo This will take 10-15 minutes. Please wait...
call npm run build:all

if errorlevel 1 (
    echo.
    echo Build had issues. Check errors above.
    pause
    exit /b 1
)

echo.
echo ========================================
echo BUILD COMPLETE!
echo ========================================
echo.
echo Installers created in dist\ folder:
dir /b dist\*.msi 2>nul
dir /b dist\*.exe 2>nul
echo.
echo Setup complete! You can now distribute the installers.
echo.
pause


