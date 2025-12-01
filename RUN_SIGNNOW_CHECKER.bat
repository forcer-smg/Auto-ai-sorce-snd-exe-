@echo off
echo ========================================
echo SignNow.com Login Checker
echo ========================================
echo.

REM Check if combo.txt exists
if not exist "combo.txt" (
    echo [!] Error: combo.txt not found!
    echo.
    echo Please create combo.txt with format:
    echo   email:password
    echo   or
    echo   email^|password
    echo.
    echo Example:
    echo   user@example.com:password123
    echo   another@example.com:pass456
    echo.
    pause
    exit /b 1
)

echo [*] Found combo.txt
echo [*] Starting checker...
echo.

REM Run the checker
python signnow_checker.py combo.txt -o signnow_results.json

echo.
echo ========================================
echo Check complete!
echo Results saved to: signnow_results.json
echo ========================================
pause

