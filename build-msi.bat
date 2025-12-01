@echo off
echo ========================================
echo BUILDING MSI INSTALLER
echo ========================================
echo.

cd /d "C:\Users\Administrator\Auto_Punch IDE"

echo [1/4] Checking disk space...
for /f "tokens=3" %%a in ('dir /-c ^| findstr /i "bytes free"') do set FREESPACE=%%a
echo   Checking available space...
echo   Note: MSI builds require at least 2 GB free space
echo.

echo [2/4] Verifying Node.js...
set "NODE_EXE="
set "NPM_EXE="
set "NODE_FOUND=0"

where node >nul 2>&1
if %errorlevel% equ 0 (
    set "NODE_EXE=node"
    set "NPM_EXE=npm"
    set "NODE_FOUND=1"
    echo   Node.js found in PATH
)

if %NODE_FOUND% equ 0 (
    if exist "C:\Program Files\nodejs\node.exe" (
        set "NODE_EXE=C:\Program Files\nodejs\node.exe"
        set "NPM_EXE=C:\Program Files\nodejs\npm.cmd"
        set "PATH=%PATH%;C:\Program Files\nodejs"
        set "NODE_FOUND=1"
        echo   Found Node.js in Program Files
    )
)

if %NODE_FOUND% equ 0 (
    echo   ERROR: Node.js not found!
    pause
    exit /b 1
)

"%NODE_EXE%" --version
echo   Node.js ready.
echo.

echo [3/4] Cleaning old MSI build files...
if exist "dist\__msi-*" (
    rmdir /s /q "dist\__msi-*" >nul 2>&1
    echo   Cleaned old MSI build files
)
if exist "dist\*.msi" (
    del /q "dist\*.msi" >nul 2>&1
    echo   Removed old MSI files
)
echo.

echo [4/4] Building MSI installer...
echo   This will take 10-15 minutes...
echo   MSI installers are better for enterprise deployment
echo.
call "%NPM_EXE%" run build:msi

if %errorlevel% neq 0 (
    echo.
    echo   ERROR: MSI build failed!
    echo.
    echo   Common issues:
    echo     1. Icon file missing (we removed icon references)
    echo     2. WiX toolset issues
    echo     3. Insufficient disk space
    echo.
    echo   Try EXE installer instead:
    echo     npm run build:exe
    pause
    exit /b 1
)

echo.
echo ========================================
echo MSI BUILD COMPLETE!
echo ========================================
echo.

if exist "dist\*.msi" (
    for %%F in ("dist\*.msi") do (
        echo MSI Installer:
        echo   File: %%~nxF
        echo   Size: %%~zF bytes
        echo   Location: %%~fF
    )
) else (
    echo   WARNING: MSI file not found in dist folder
)

echo.
echo Opening dist folder...
timeout /t 1 /nobreak >nul
start explorer dist

echo.
pause


