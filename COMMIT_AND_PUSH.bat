@echo off
echo ========================================
echo Auto_Punch IDE - Git Commit and Push
echo ========================================
echo.

cd /d "%~dp0"

echo [1/5] Checking Git status...
git status
echo.

echo [2/5] Adding all files...
git add .
echo.

echo [3/5] Creating commit...
git commit -m "WIP: Auto_Punch IDE - AI code generation, terminal execution, file creation features

Features added:
- AI code generation with automatic file creation
- Terminal command execution in dashboard
- File auto-detection and editor opening
- Enhanced code block parsing
- Terminal output filtering
- Batch file execution handling

Known issues:
- Terminal integration for batch files needs fix (outputs to background terminal)
- Need to route all terminal output to dashboard terminal panel"
echo.

echo [4/5] Checking remote repository...
git remote -v
echo.

echo [5/5] Ready to push!
echo.
echo If remote is not set, run:
echo   git remote add origin YOUR_GITHUB_REPO_URL
echo.
echo Then push with:
echo   git push -u origin main
echo   OR
echo   git push -u origin master
echo.

pause

