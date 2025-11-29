@echo off
echo ========================================
echo Auto_Punch IDE - GitHub Setup for SMG-Dawn
echo ========================================
echo.

cd /d "%~dp0"

echo [1/4] Configuring Git user...
git config user.name "SMG-Dawn"
git config user.email "beecher8080@gmail.com"
echo ✓ Git user configured:
git config user.name
git config user.email
echo.

echo [2/4] Initializing Git repository...
if not exist .git (
    git init
    echo ✓ Git repository initialized
) else (
    echo ✓ Git repository already initialized
)
echo.

echo [3/4] Checking existing remotes...
git remote -v
echo.

echo [4/4] Adding GitHub remote...
echo.
echo Please provide your GitHub repository name.
echo Examples:
echo   - Auto_Punch-IDE
echo   - auto-punch-ide
echo   - AutoPunchIDE
echo.
set /p REPO_NAME="Enter your repository name (or full URL): "

if "%REPO_NAME%"=="" (
    echo No repository name provided.
    echo.
    echo You can add the remote manually later with:
    echo   git remote add origin https://github.com/SMG-Dawn/YOUR_REPO_NAME.git
    pause
    exit /b 0
)

REM Check if it's a full URL or just repo name
echo %REPO_NAME% | findstr /C:"github.com" >nul
if errorlevel 1 (
    REM It's just a repo name, construct the URL
    set GITHUB_URL=https://github.com/SMG-Dawn/%REPO_NAME%.git
) else (
    REM It's already a full URL
    set GITHUB_URL=%REPO_NAME%
)

echo.
echo Adding remote 'origin' with URL: %GITHUB_URL%
git remote remove origin >nul 2>&1
git remote add origin %GITHUB_URL%
echo ✓ Remote added successfully
echo.

echo [Verification] Current remotes:
git remote -v
echo.

echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Your Git configuration:
echo   Username: SMG-Dawn
echo   Email: beecher8080@gmail.com
echo   Remote: %GITHUB_URL%
echo.
echo Next steps:
echo   1. Make sure the repository exists on GitHub
echo      https://github.com/SMG-Dawn/%REPO_NAME%
echo.
echo   2. Add and commit your files:
echo      git add .
echo      git commit -m "Initial commit: Auto_Punch IDE"
echo.
echo   3. Push to GitHub:
echo      git branch -M main
echo      git push -u origin main
echo.
echo   Note: For private repos, you'll need to authenticate
echo   using a Personal Access Token or SSH key.
echo.
pause

