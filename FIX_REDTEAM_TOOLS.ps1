# Fix RedTeam-Tools Git Repository Issue
Write-Host "Fixing RedTeam-Tools embedded repository..." -ForegroundColor Yellow

Set-Location "C:\Users\Administrator\Auto_Punch IDE"

# Remove .git from RedTeam-Tools to include it as regular files
if (Test-Path "RedTeam-Tools\.git") {
    Write-Host "[~] Removing .git from RedTeam-Tools..." -ForegroundColor Yellow
    Remove-Item -Path "RedTeam-Tools\.git" -Recurse -Force
    Write-Host "[+] RedTeam-Tools .git removed" -ForegroundColor Green
    Write-Host ""
    Write-Host "RedTeam-Tools will now be included as regular files in the repository." -ForegroundColor Cyan
    Write-Host "Run: git add RedTeam-Tools" -ForegroundColor Yellow
    Write-Host "Then: git commit -m 'Include RedTeam-Tools files'" -ForegroundColor Yellow
} else {
    Write-Host "[+] RedTeam-Tools .git already removed" -ForegroundColor Green
}

