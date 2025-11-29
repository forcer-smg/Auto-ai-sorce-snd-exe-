@echo off
setlocal enabledelayedexpansion

echo.
echo ========================================
echo Quick Image Upload
echo ========================================
echo.

set "SOURCE=C:\Users\Administrator\Downloads\tai.jpeg"
set "DEST=%~dp0static\images\hacking-bg.jpg"

echo Copying: %SOURCE%
echo To: %DEST%
echo.

if not exist "%SOURCE%" (
    echo [ERROR] Source file not found: %SOURCE%
    echo.
    pause
    exit /b 1
)

if not exist "%~dp0static\images" (
    mkdir "%~dp0static\images"
)

copy /Y "%SOURCE%" "%DEST%"

if exist "%DEST%" (
    echo.
    echo [SUCCESS] Image uploaded!
    echo File: %DEST%
    echo.
    echo Now:
    echo 1. Restart server
    echo 2. Ctrl+Shift+R in browser
    echo 3. Enable Hacking theme
    echo.
) else (
    echo.
    echo [ERROR] Upload failed!
    echo.
)

pause

