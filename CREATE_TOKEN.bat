@echo off
echo ========================================
echo GitHub Personal Access Token Guide
echo ========================================
echo.
echo This will open GitHub in your browser to create a token.
echo.
echo Steps:
echo   1. Browser will open to GitHub token creation page
echo   2. Name: Auto_Punch IDE
echo   3. Expiration: Choose 90 days or No expiration
echo   4. Scope: Check 'repo' (full control of private repositories)
echo   5. Click 'Generate token'
echo   6. COPY THE TOKEN IMMEDIATELY (you won't see it again!)
echo.
pause

echo.
echo Opening GitHub token creation page...
start https://github.com/settings/tokens/new

echo.
echo ========================================
echo After creating your token:
echo ========================================
echo.
echo 1. Copy the token (starts with 'ghp_')
echo 2. Save it somewhere safe
echo 3. When pushing to GitHub:
echo    - Username: SMG-Dawn
echo    - Password: Paste your token (NOT your GitHub password)
echo.
echo To push your code, run: PUSH_TO_GITHUB.bat
echo.
pause

