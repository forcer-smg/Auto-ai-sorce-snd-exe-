# Prepare for GitHub Upload
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  PREPARING FOR GITHUB UPLOAD" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

Set-Location "C:\Users\Administrator\Auto_Punch IDE"

# Check if git is initialized
if (-not (Test-Path ".git")) {
    Write-Host "[!] Git not initialized. Initializing..." -ForegroundColor Yellow
    git init
    Write-Host "[+] Git initialized" -ForegroundColor Green
}

# Check git status
Write-Host "[~] Checking git status..." -ForegroundColor Yellow
$status = git status --porcelain
if ($status) {
    Write-Host "[+] Found changes to commit" -ForegroundColor Green
    Write-Host ""
    Write-Host "Changes:" -ForegroundColor Cyan
    git status --short
} else {
    Write-Host "[+] No uncommitted changes" -ForegroundColor Green
}

# Check if remote exists
Write-Host ""
Write-Host "[~] Checking remote repository..." -ForegroundColor Yellow
$remote = git remote -v
if ($remote) {
    Write-Host "[+] Remote configured:" -ForegroundColor Green
    Write-Host $remote
} else {
    Write-Host "[!] No remote repository configured" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "To add remote, run:" -ForegroundColor Cyan
    Write-Host "  git remote add origin <your-repo-url>" -ForegroundColor White
}

# Find built executable
Write-Host ""
Write-Host "[~] Looking for built executable..." -ForegroundColor Yellow
$exePath = "dist\Auto_Punch IDE Setup 1.0.0.exe"
$unpackedExe = "dist\win-unpacked\Auto_Punch IDE.exe"

if (Test-Path $exePath) {
    $exeSize = (Get-Item $exePath).Length / 1MB
    Write-Host "[+] Found installer: $exePath ($([math]::Round($exeSize, 2)) MB)" -ForegroundColor Green
} elseif (Test-Path $unpackedExe) {
    $exeSize = (Get-Item $unpackedExe).Length / 1MB
    Write-Host "[+] Found executable: $unpackedExe ($([math]::Round($exeSize, 2)) MB)" -ForegroundColor Green
} else {
    Write-Host "[!] No built executable found. Run build first." -ForegroundColor Red
    exit 1
}

# Create release notes
Write-Host ""
Write-Host "[~] Creating release notes..." -ForegroundColor Yellow
$releaseNotes = @"
# Auto_Punch IDE v1.0.0 Release

## Features
- ✅ Full IDE with VS Code + Cursor features
- ✅ Auto_Punch Ai integration
- ✅ RedTeam Toolkit (138 tools)
- ✅ Telegram integration (Railway + Supabase)
- ✅ Settings sync
- ✅ Desktop app registration

## Fixes
- ✅ Toolkit frontend error fixed
- ✅ Tool discovery improved (365-Stealer, requests-ip-rotator)
- ✅ CSS 404 errors fixed
- ✅ Python detection improved
- ✅ Unicode encoding fixed
- ✅ Browser auto-open fixed

## Tools Added
- 365-Stealer (Initial Access)
- requests-ip-rotator (Defense Evasion)

## Installation
1. Download `Auto_Punch IDE Setup 1.0.0.exe`
2. Run the installer
3. Ensure Python 3.11+ is installed
4. Launch Auto_Punch IDE

## Requirements
- Windows 10/11
- Python 3.11 or later
- Node.js (for development)

## Notes
- First run may take time to initialize Auto_Punch Ai components
- Telegram bot requires TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID
- Supabase requires SUPABASE_URL and SUPABASE_KEY for settings sync
"@

$releaseNotes | Out-File -FilePath "RELEASE_NOTES.md" -Encoding UTF8
Write-Host "[+] Release notes created: RELEASE_NOTES.md" -ForegroundColor Green

Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host "  READY FOR GITHUB UPLOAD" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Review changes: git status" -ForegroundColor White
Write-Host "2. Add files: git add ." -ForegroundColor White
Write-Host "3. Commit: git commit -m 'Release v1.0.0 - All fixes applied'" -ForegroundColor White
Write-Host "4. Push: git push origin main" -ForegroundColor White
Write-Host "5. Create GitHub Release and upload: $exePath" -ForegroundColor White
Write-Host ""
Write-Host "Or run: .\COMMIT_AND_PUSH.ps1" -ForegroundColor Yellow

