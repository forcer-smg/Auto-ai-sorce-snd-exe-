@echo off
echo ========================================
echo Auto_Punch IDE - Push to GitHub
echo Repository: SMG-Dawn/Auto-pounch-ai
echo ========================================
echo.

cd /d "%~dp0"

echo [1/4] Checking Git status...
git status
echo.

echo [2/4] Adding all files...
git add .
echo ✓ Files added
echo.

echo [3/4] Creating commit...
git commit -m "WIP: Auto_Punch IDE - AI code generation, terminal execution, file creation features

Features added:
- AI code generation with automatic file creation
- Terminal command execution in dashboard
- File auto-detection and editor opening
- Enhanced code block parsing
- Terminal output filtering
- Batch file execution handling
- GitHub integration setup

Known issues:
- Terminal integration for batch files needs fix (outputs to background terminal)
- Need to route all terminal output to dashboard terminal panel"
echo.

echo [4/4] Pushing to GitHub...
echo.
echo NOTE: Since this is a private repository, you'll need to authenticate.
echo.
echo If using HTTPS, you'll need a Personal Access Token:
echo   1. Go to: https://github.com/settings/tokens
echo   2. Generate new token (classic) with 'repo' scope
echo   3. Use the token as your password when prompted
echo.
echo If using SSH, make sure your SSH key is added to GitHub.
echo.

set /p PUSH_NOW="Push to GitHub now? (y/n): "
if /i "%PUSH_NOW%"=="y" (
    echo.
    echo Pushing to origin main...
    git branch -M main 2>nul
    git push -u origin main
    echo.
    if errorlevel 1 (
        echo.
        echo Push failed. This might be due to:
        echo   - Authentication required (use Personal Access Token)
        echo   - Repository doesn't exist yet
        echo   - Network issues
        echo.
        echo Try pushing manually:
        echo   git push -u origin main
    ) else (
        echo.
        echo ✓ Successfully pushed to GitHub!
        echo Repository: https://github.com/SMG-Dawn/Auto-pounch-ai
    )
) else (
    echo.
    echo To push manually later, run:
    echo   git branch -M main
    echo   git push -u origin main
)

echo.
pause

