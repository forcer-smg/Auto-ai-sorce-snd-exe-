@echo off
echo ========================================
echo Finding Image Files on Your System
echo ========================================
echo.
echo Searching common locations for image files...
echo.

echo Checking Downloads folder...
if exist "%USERPROFILE%\Downloads\*.jpg" (
    echo.
    echo JPG files found in Downloads:
    dir /b "%USERPROFILE%\Downloads\*.jpg"
    echo.
)
if exist "%USERPROFILE%\Downloads\*.png" (
    echo PNG files found in Downloads:
    dir /b "%USERPROFILE%\Downloads\*.png"
    echo.
)

echo Checking Desktop...
if exist "%USERPROFILE%\Desktop\*.jpg" (
    echo.
    echo JPG files found on Desktop:
    dir /b "%USERPROFILE%\Desktop\*.jpg"
    echo.
)
if exist "%USERPROFILE%\Desktop\*.png" (
    echo PNG files found on Desktop:
    dir /b "%USERPROFILE%\Desktop\*.png"
    echo.
)

echo Checking Pictures folder...
if exist "%USERPROFILE%\Pictures\*.jpg" (
    echo.
    echo JPG files found in Pictures:
    dir /b "%USERPROFILE%\Pictures\*.jpg" | more
    echo.
)
if exist "%USERPROFILE%\Pictures\*.png" (
    echo PNG files found in Pictures:
    dir /b "%USERPROFILE%\Pictures\*.png" | more
    echo.
)

echo ========================================
echo.
echo If you see your image file above, copy the FULL PATH
echo and use it with PLACE_BACKGROUND_IMAGE.bat
echo.
echo Example: C:\Users\Administrator\Downloads\my-image.jpg
echo.
pause

