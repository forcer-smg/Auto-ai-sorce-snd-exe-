@echo off
echo ========================================
echo Auto_Punch IDE - GitHub Connection Setup
echo ========================================
echo.

cd /d "%~dp0"

echo [Step 1] Checking Git installation...
git --version
if errorlevel 1 (
    echo ERROR: Git is not installed or not in PATH
    echo Please install Git from https://git-scm.com/
    pause
    exit /b 1
)
echo.

echo [Step 2] Checking if Git is initialized...
if not exist .git (
    echo Initializing Git repository...
    git init
    echo Git repository initialized!
) else (
    echo Git repository already initialized.
)
echo.

echo [Step 3] Checking Git user configuration...
git config user.name >nul 2>&1
if errorlevel 1 (
    echo Git user name is not set.
    set /p GIT_USERNAME="Enter your Git username: "
    git config user.name "%GIT_USERNAME%"
    echo User name set to: %GIT_USERNAME%
) else (
    echo Current Git user name: 
    git config user.name
)

git config user.email >nul 2>&1
if errorlevel 1 (
    echo Git user email is not set.
    set /p GIT_EMAIL="Enter your Git email: "
    git config user.email "%GIT_EMAIL%"
    echo User email set to: %GIT_EMAIL%
) else (
    echo Current Git user email:
    git config user.email
)
echo.

echo [Step 4] Checking existing remotes...
git remote -v
echo.

echo [Step 5] Adding GitHub remote...
echo.
echo Please provide your GitHub repository URL.
echo Examples:
echo   HTTPS: https://github.com/username/repo-name.git
echo   SSH:   git@github.com:username/repo-name.git
echo.
set /p GITHUB_URL="Enter your GitHub repository URL: "

if "%GITHUB_URL%"=="" (
    echo No URL provided. Exiting.
    pause
    exit /b 1
)

echo.
echo Adding remote 'origin' with URL: %GITHUB_URL%
git remote remove origin >nul 2>&1
git remote add origin %GITHUB_URL%
echo.

echo [Step 6] Verifying connection...
git remote -v
echo.

echo [Step 7] Testing connection...
echo Attempting to fetch from remote (this will test authentication)...
git fetch origin
if errorlevel 1 (
    echo.
    echo WARNING: Could not fetch from remote.
    echo This might be because:
    echo   1. Repository doesn't exist yet (create it on GitHub first)
    echo   2. Authentication is required (use GitHub Personal Access Token)
    echo   3. Repository is private and needs authentication
    echo.
    echo For private repos, you may need to:
    echo   - Use SSH keys, OR
    echo   - Use Personal Access Token with HTTPS
    echo.
) else (
    echo SUCCESS: Connection to GitHub verified!
)
echo.

echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo   1. If repository doesn't exist, create it on GitHub first
echo   2. Add and commit your files: git add . ^&^& git commit -m "Initial commit"
echo   3. Push to GitHub: git push -u origin main
echo.
pause

