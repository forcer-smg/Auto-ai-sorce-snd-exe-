@echo off
echo ========================================
echo Uploading Background Image
echo ========================================
echo.

set SOURCE=C:\Users\Administrator\Downloads\tai.jpeg
set DEST=C:\Users\Administrator\Auto_Punch IDE\static\images\hacking-bg.jpg

echo Source: %SOURCE%
echo Destination: %DEST%
echo.

if not exist "%SOURCE%" (
    echo ERROR: Source file not found!
    echo Please check: %SOURCE%
    pause
    exit /b 1
)

if not exist "static\images" mkdir "static\images"

echo Copying file...
copy /Y "%SOURCE%" "%DEST%" >nul 2>&1

if exist "%DEST%" (
    echo.
    echo ========================================
    echo SUCCESS! Image uploaded!
    echo ========================================
    echo.
    echo File: hacking-bg.jpg
    echo Location: static\images\
    echo.
    echo Next steps:
    echo 1. Restart IDE server
    echo 2. Hard refresh browser: Ctrl+Shift+R
    echo 3. Settings -^> Theme -^> Hacking Mode
    echo.
) else (
    echo.
    echo ERROR: Failed to copy file
    echo.
    echo Try running as Administrator
    echo.
)

pause

