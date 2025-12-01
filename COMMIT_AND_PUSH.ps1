# Commit and Push to GitHub
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  COMMITTING AND PUSHING TO GITHUB" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

Set-Location "C:\Users\Administrator\Auto_Punch IDE"

# Check if there are changes
$status = git status --porcelain
if (-not $status) {
    Write-Host "[!] No changes to commit" -ForegroundColor Yellow
    exit 0
}

# Show what will be committed
Write-Host "[~] Changes to commit:" -ForegroundColor Yellow
git status --short
Write-Host ""

# Add all files
Write-Host "[~] Adding files..." -ForegroundColor Yellow
git add .

# Commit
$commitMessage = "Release v1.0.0 - All fixes applied

- Toolkit frontend error fixed
- Tool discovery improved (365-Stealer, requests-ip-rotator)
- CSS 404 errors fixed
- Python detection improved
- Unicode encoding fixed
- Browser auto-open fixed
- Telegram integration ready
- Settings sync ready"

Write-Host "[~] Committing changes..." -ForegroundColor Yellow
git commit -m $commitMessage

if ($LASTEXITCODE -eq 0) {
    Write-Host "[+] Changes committed" -ForegroundColor Green
    
    # Check remote
    $remote = git remote get-url origin 2>$null
    if ($remote) {
        Write-Host ""
        Write-Host "[~] Pushing to GitHub..." -ForegroundColor Yellow
        $branch = git branch --show-current
        if (-not $branch) {
            $branch = "main"
            git branch -M main
        }
        
        git push origin $branch
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host ""
            Write-Host "============================================================" -ForegroundColor Green
            Write-Host "  SUCCESSFULLY PUSHED TO GITHUB" -ForegroundColor Green
            Write-Host "============================================================" -ForegroundColor Green
            Write-Host ""
            Write-Host "Next: Create a GitHub Release and upload:" -ForegroundColor Cyan
            Write-Host "  dist\Auto_Punch IDE Setup 1.0.0.exe" -ForegroundColor White
        } else {
            Write-Host ""
            Write-Host "[!] Push failed. Check your remote configuration." -ForegroundColor Red
        }
    } else {
        Write-Host ""
        Write-Host "[!] No remote configured. Add remote first:" -ForegroundColor Yellow
        Write-Host "  git remote add origin <your-repo-url>" -ForegroundColor White
    }
} else {
    Write-Host ""
    Write-Host "[!] Commit failed" -ForegroundColor Red
}

Write-Host ""
Read-Host "Press Enter to exit"

