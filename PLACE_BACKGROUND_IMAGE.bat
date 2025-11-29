@echo off
echo ========================================
echo Auto_Punch IDE - Background Image Setup
echo ========================================
echo.
echo This script will help you place your background image.
echo.
echo Please provide the FULL PATH to your IMAGE FILE (not folder).
echo.
echo Example: C:\Users\Administrator\Downloads\my-image.jpg
echo.
echo Searching for image files in common locations...
echo.

REM Check common image locations
set FOUND=0

REM Check Downloads folder
if exist "%USERPROFILE%\Downloads\*.jpg" (
    echo Found JPG files in Downloads:
    dir /b "%USERPROFILE%\Downloads\*.jpg" 2>nul
    echo.
    set FOUND=1
)
if exist "%USERPROFILE%\Downloads\*.png" (
    echo Found PNG files in Downloads:
    dir /b "%USERPROFILE%\Downloads\*.png" 2>nul
    echo.
    set FOUND=1
)

REM Check Desktop
if exist "%USERPROFILE%\Desktop\*.jpg" (
    echo Found JPG files on Desktop:
    dir /b "%USERPROFILE%\Desktop\*.jpg" 2>nul
    echo.
    set FOUND=1
)
if exist "%USERPROFILE%\Desktop\*.png" (
    echo Found PNG files on Desktop:
    dir /b "%USERPROFILE%\Desktop\*.png" 2>nul
    echo.
    set FOUND=1
)

if %FOUND%==0 (
    echo No image files found in common locations.
    echo.
)

echo ========================================
echo.
set /p IMAGE_PATH="Enter FULL PATH to your image file: "

REM Remove quotes if user added them
set IMAGE_PATH=%IMAGE_PATH:"=%

REM Check if it's a directory
if exist "%IMAGE_PATH%" (
    if exist "%IMAGE_PATH%\*" (
        echo.
        echo ERROR: You entered a FOLDER path, not a FILE path!
        echo.
        echo Please provide the full path to the IMAGE FILE itself.
        echo Example: C:\Users\Administrator\Downloads\image.jpg
        echo.
        echo Files in that folder:
        dir /b "%IMAGE_PATH%\*.jpg" "%IMAGE_PATH%\*.png" 2>nul
        echo.
        pause
        exit /b 1
    )
)

REM Check if file exists
if not exist "%IMAGE_PATH%" (
    echo.
    echo ERROR: File not found at: %IMAGE_PATH%
    echo.
    echo Please check:
    echo 1. The file path is correct
    echo 2. The file exists
    echo 3. You included the file name and extension
    echo.
    pause
    exit /b 1
)

REM Check if it's an image file
echo "%IMAGE_PATH%" | findstr /i "\.jpg \.jpeg \.png \.gif \.webp" >nul
if errorlevel 1 (
    echo.
    echo WARNING: File doesn't have a common image extension (.jpg, .png, etc.)
    echo Continue anyway? (Y/N)
    set /p CONTINUE=
    if /i not "%CONTINUE%"=="Y" exit /b 1
)

echo.
echo Copying image...
if not exist "static\images" mkdir "static\images"

REM Get file extension
for %%F in ("%IMAGE_PATH%") do set EXT=%%~xF

REM Copy with appropriate extension
copy "%IMAGE_PATH%" "static\images\hacking-bg%EXT%" >nul 2>&1

if exist "static\images\hacking-bg%EXT%" (
    echo.
    echo ========================================
    echo SUCCESS! Image placed successfully!
    echo ========================================
    echo.
    echo File copied to: static\images\hacking-bg%EXT%
    echo.
    echo Next steps:
    echo 1. Restart the IDE server (if running)
    echo 2. Hard refresh browser: Ctrl + Shift + R
    echo 3. Go to Settings -^> Appearance -^> Theme
    echo 4. Select "Hacking Mode (Cyberpunk)"
    echo.
    echo The background image will appear automatically!
    echo.
) else (
    echo.
    echo ========================================
    echo ERROR: Failed to copy image
    echo ========================================
    echo.
    echo Possible reasons:
    echo 1. File permissions issue
    echo 2. File is locked by another program
    echo 3. Disk space issue
    echo.
    echo Try:
    echo - Close any programs using the image
    echo - Run this script as Administrator
    echo - Check available disk space
    echo.
)

pause

