@echo off
echo ========================================
echo SYSTEM CHECK FOR BUILD
echo ========================================
echo.

cd /d "%~dp0"

echo [1/6] Checking Node.js...
where node >nul 2>&1
if %errorlevel% equ 0 (
    node --version
    echo   Node.js: OK
) else (
    if exist "C:\Program Files\nodejs\node.exe" (
        "C:\Program Files\nodejs\node.exe" --version
        echo   Node.js: Found in Program Files
    ) else (
        echo   ERROR: Node.js not found!
        echo   Install from: https://nodejs.org/
        set "HAS_ERROR=1"
    )
)
echo.

echo [2/6] Checking npm...
where npm >nul 2>&1
if %errorlevel% equ 0 (
    npm --version
    echo   npm: OK
) else (
    if exist "C:\Program Files\nodejs\npm.cmd" (
        "C:\Program Files\nodejs\npm.cmd" --version
        echo   npm: Found in Program Files
    ) else (
        echo   ERROR: npm not found!
        set "HAS_ERROR=1"
    )
)
echo.

echo [3/6] Checking Python...
where python >nul 2>&1
if %errorlevel% equ 0 (
    python --version
    echo   Python: OK
) else (
    echo   WARNING: Python not found
    echo   Needed for Flask backend
)
echo.

echo [4/6] Checking disk space...
for /f "tokens=3" %%a in ('dir /-c ^| findstr /i "bytes free"') do set FREESPACE=%%a
echo   Checking available space...
echo   Note: Need at least 2 GB free for build
echo.

echo [5/6] Checking required files...
if exist "package.json" (
    echo   package.json: OK
) else (
    echo   ERROR: package.json missing!
    set "HAS_ERROR=1"
)

if exist "electron\main.js" (
    echo   electron\main.js: OK
) else (
    echo   ERROR: electron\main.js missing!
    set "HAS_ERROR=1"
)

if exist "app.py" (
    echo   app.py: OK
) else (
    echo   ERROR: app.py missing!
    set "HAS_ERROR=1"
)
echo.

echo [6/6] Checking dependencies...
if exist "node_modules\electron" (
    echo   Electron: Installed
) else (
    echo   WARNING: Electron not installed
    echo   Run: npm install
)

if exist "node_modules\electron-builder" (
    echo   electron-builder: Installed
) else (
    echo   WARNING: electron-builder not installed
    echo   Run: npm install
)
echo.

echo ========================================
if defined HAS_ERROR (
    echo SYSTEM CHECK: ERRORS FOUND
    echo ========================================
    echo.
    echo Please fix the errors above before building.
) else (
    echo SYSTEM CHECK: READY
    echo ========================================
    echo.
    echo Your system is ready to build!
    echo.
    echo Next step: .\BUILD_ROBUST.bat
)
echo.
pause


