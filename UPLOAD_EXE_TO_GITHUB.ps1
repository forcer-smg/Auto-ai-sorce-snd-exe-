# Upload EXE to Different GitHub Repository
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  UPLOAD EXE TO GITHUB REPOSITORY" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

Set-Location "C:\Users\Administrator\Auto_Punch IDE"

# Find the executable
$exePath = "dist\Auto_Punch IDE Setup 1.0.0.exe"
$unpackedExe = "dist\win-unpacked\Auto_Punch IDE.exe"

$exeFile = $null
if (Test-Path $exePath) {
    $exeFile = $exePath
    $exeSize = (Get-Item $exePath).Length / 1MB
    Write-Host "[+] Found installer: $exePath ($([math]::Round($exeSize, 2)) MB)" -ForegroundColor Green
} elseif (Test-Path $unpackedExe) {
    $exeFile = $unpackedExe
    $exeSize = (Get-Item $unpackedExe).Length / 1MB
    Write-Host "[+] Found executable: $unpackedExe ($([math]::Round($exeSize, 2)) MB)" -ForegroundColor Green
} else {
    Write-Host "[!] No executable found. Run build first." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Enter GitHub repository details:" -ForegroundColor Yellow
Write-Host ""

# Get repository info
$repoOwner = Read-Host "Repository Owner/Username (e.g., SMG-Dawn)"
$repoName = Read-Host "Repository Name (e.g., Auto-Punch-IDE-Releases)"
$repoUrl = "https://github.com/$repoOwner/$repoName"

Write-Host ""
Write-Host "Repository: $repoUrl" -ForegroundColor Cyan
Write-Host ""

# Check if git is available
$gitAvailable = Get-Command git -ErrorAction SilentlyContinue
if (-not $gitAvailable) {
    Write-Host "[!] Git is not installed or not in PATH" -ForegroundColor Red
    Write-Host ""
    Write-Host "Options:" -ForegroundColor Yellow
    Write-Host "1. Install Git and try again" -ForegroundColor White
    Write-Host "2. Upload manually via GitHub web interface" -ForegroundColor White
    Write-Host ""
    Write-Host "For manual upload:" -ForegroundColor Cyan
    Write-Host "1. Go to: $repoUrl/releases/new" -ForegroundColor White
    Write-Host "2. Create a new release (tag: v1.0.0)" -ForegroundColor White
    Write-Host "3. Upload: $exeFile" -ForegroundColor White
    exit 1
}

# Check if repository exists locally or needs to be cloned
$tempRepoPath = "$env:TEMP\Auto_Punch_IDE_Release_Upload"
if (Test-Path $tempRepoPath) {
    Write-Host "[~] Cleaning up previous temp repository..." -ForegroundColor Yellow
    Remove-Item -Path $tempRepoPath -Recurse -Force -ErrorAction SilentlyContinue
}

Write-Host ""
Write-Host "[~] Cloning repository..." -ForegroundColor Yellow
try {
    git clone "https://github.com/$repoOwner/$repoName.git" $tempRepoPath 2>&1 | Out-Null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[!] Failed to clone repository. Check:" -ForegroundColor Red
        Write-Host "   - Repository exists: $repoUrl" -ForegroundColor White
        Write-Host "   - You have access" -ForegroundColor White
        Write-Host "   - Repository is public or you're authenticated" -ForegroundColor White
        Write-Host ""
        Write-Host "Alternative: Upload manually via GitHub web interface" -ForegroundColor Yellow
        Write-Host "1. Go to: $repoUrl/releases/new" -ForegroundColor White
        Write-Host "2. Create release and upload: $exeFile" -ForegroundColor White
        exit 1
    }
    Write-Host "[+] Repository cloned" -ForegroundColor Green
} catch {
    Write-Host "[!] Error cloning repository: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please upload manually:" -ForegroundColor Yellow
    Write-Host "1. Go to: $repoUrl/releases/new" -ForegroundColor White
    Write-Host "2. Upload: $exeFile" -ForegroundColor White
    exit 1
}

# Copy executable to releases directory
Set-Location $tempRepoPath

# Create releases directory if it doesn't exist
$releasesDir = "releases"
if (-not (Test-Path $releasesDir)) {
    New-Item -ItemType Directory -Path $releasesDir | Out-Null
}

# Copy executable
$exeName = Split-Path $exeFile -Leaf
$destPath = Join-Path $releasesDir $exeName
Copy-Item -Path (Resolve-Path $exeFile) -Destination $destPath -Force
Write-Host "[+] Copied executable to repository" -ForegroundColor Green

# Create or update README
$readmeContent = @"
# Auto_Punch IDE Releases

## Latest Release

### Version 1.0.0

**Download:** [$exeName](./releases/$exeName)

**Release Date:** $(Get-Date -Format "yyyy-MM-dd")

## Installation

1. Download the installer
2. Run `$exeName`
3. Follow the installation wizard
4. Launch Auto_Punch IDE

## Requirements

- Windows 10/11
- Python 3.11 or later
- Node.js (for development)

## Features

- Full IDE with VS Code + Cursor features
- Auto_Punch Ai integration
- RedTeam Toolkit (138 tools)
- Telegram integration
- Settings sync
- Desktop app registration

## Notes

- First run may take time to initialize
- Ensure Python is in your PATH
- Telegram bot requires configuration for notifications
"@

Set-Content -Path "README.md" -Value $readmeContent
Write-Host "[+] Created README.md" -ForegroundColor Green

# Commit and push
Write-Host ""
Write-Host "[~] Committing changes..." -ForegroundColor Yellow
git add .
git commit -m "Add Auto_Punch IDE v1.0.0 release" 2>&1 | Out-Null

if ($LASTEXITCODE -eq 0) {
    Write-Host "[+] Changes committed" -ForegroundColor Green
    
    Write-Host "[~] Pushing to GitHub..." -ForegroundColor Yellow
    git push origin main 2>&1 | Out-Null
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "============================================================" -ForegroundColor Green
        Write-Host "  SUCCESSFULLY UPLOADED TO GITHUB" -ForegroundColor Green
        Write-Host "============================================================" -ForegroundColor Green
        Write-Host ""
        Write-Host "Repository: $repoUrl" -ForegroundColor Cyan
        Write-Host "File: releases/$exeName" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "Next steps:" -ForegroundColor Yellow
        Write-Host "1. Go to: $repoUrl/releases/new" -ForegroundColor White
        Write-Host "2. Create a new release (tag: v1.0.0)" -ForegroundColor White
        Write-Host "3. Attach the executable as a release asset" -ForegroundColor White
        Write-Host "4. Or the file is already in the repository at: releases/$exeName" -ForegroundColor White
    } else {
        Write-Host ""
        Write-Host "[!] Push failed. You may need to:" -ForegroundColor Yellow
        Write-Host "   - Authenticate with GitHub" -ForegroundColor White
        Write-Host "   - Check repository permissions" -ForegroundColor White
        Write-Host ""
        Write-Host "File is ready at: $destPath" -ForegroundColor Cyan
        Write-Host "You can manually upload it via GitHub web interface" -ForegroundColor Yellow
    }
} else {
    Write-Host "[!] Commit failed" -ForegroundColor Red
    Write-Host "File is ready at: $destPath" -ForegroundColor Cyan
}

# Cleanup
Set-Location "C:\Users\Administrator\Auto_Punch IDE"
Write-Host ""
Write-Host "[~] Cleaning up..." -ForegroundColor Yellow
Remove-Item -Path $tempRepoPath -Recurse -Force -ErrorAction SilentlyContinue

Write-Host ""
Read-Host "Press Enter to exit"

