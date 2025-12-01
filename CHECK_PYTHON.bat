@echo off
REM ============================================================
REM CHECK PYTHON INSTALLATION
REM ============================================================

echo.
echo ============================================================
echo   CHECKING PYTHON INSTALLATION
echo ============================================================
echo.

REM Check if python is in PATH
where python >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [+] Python found in PATH
    python --version
    echo.
    where python
    echo.
) else (
    echo [!] Python NOT found in PATH
    echo.
)

REM Check if py launcher is available
where py >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [+] Python Launcher (py) found
    py --version
    echo.
    where py
    echo.
) else (
    echo [!] Python Launcher (py) NOT found
    echo.
)

REM Check common Python installation paths
echo [~] Checking common Python installation paths...
echo.

set PYTHON_PATHS=C:\Python314\python.exe C:\Python313\python.exe C:\Python312\python.exe C:\Python311\python.exe C:\Python310\python.exe "C:\Program Files\Python314\python.exe" "C:\Program Files\Python313\python.exe" "C:\Program Files\Python312\python.exe" "C:\Program Files\Python311\python.exe"

for %%P in (%PYTHON_PATHS%) do (
    if exist %%P (
        echo [+] Found: %%P
        %%P --version
    )
)

echo.
echo ============================================================
echo   RECOMMENDATIONS
echo ============================================================
echo.
echo If Python is not found:
echo   1. Install Python from https://www.python.org/downloads/
echo   2. During installation, check "Add Python to PATH"
echo   3. Restart your computer
echo   4. Run this script again to verify
echo.
pause

