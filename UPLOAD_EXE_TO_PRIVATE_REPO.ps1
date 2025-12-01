# Upload EXE to Private GitHub Repository
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  UPLOAD EXE TO PRIVATE GITHUB REPOSITORY" -ForegroundColor Cyan
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
Write-Host "============================================================" -ForegroundColor Yellow
Write-Host "  PRIVATE REPOSITORY SETUP" -ForegroundColor Yellow
Write-Host "============================================================" -ForegroundColor Yellow
Write-Host ""

# Check authentication methods
$ghAvailable = Get-Command gh -ErrorAction SilentlyContinue
$gitAvailable = Get-Command git -ErrorAction SilentlyContinue

if (-not $gitAvailable) {
    Write-Host "[!] Git is not installed" -ForegroundColor Red
    Write-Host "Download from: https://git-scm.com/download/win" -ForegroundColor Yellow
    exit 1
}

Write-Host "[+] Git found" -ForegroundColor Green

if ($ghAvailable) {
    Write-Host "[+] GitHub CLI found" -ForegroundColor Green
    Write-Host ""
    Write-Host "Option 1: Use GitHub CLI (Recommended - handles auth automatically)" -ForegroundColor Cyan
    Write-Host "Option 2: Use Git directly (requires manual authentication)" -ForegroundColor Cyan
    Write-Host ""
    $useGH = Read-Host "Use GitHub CLI? (Y/n)"
    
    if ($useGH -eq "" -or $useGH -eq "Y" -or $useGH -eq "y") {
        # Use GitHub CLI
        Write-Host ""
        Write-Host "[~] Checking GitHub CLI authentication..." -ForegroundColor Yellow
        $authStatus = gh auth status 2>&1
        if ($LASTEXITCODE -ne 0) {
            Write-Host "[!] Not authenticated. Starting authentication..." -ForegroundColor Yellow
            gh auth login
        } else {
            Write-Host "[+] Authenticated with GitHub CLI" -ForegroundColor Green
        }
        
        Write-Host ""
        Write-Host "Repository options:" -ForegroundColor Yellow
        Write-Host "1. Create new private repository" -ForegroundColor White
        Write-Host "2. Use existing repository" -ForegroundColor White
        Write-Host ""
        $option = Read-Host "Choose option (1/2)"
        
        if ($option -eq "1") {
            $repoName = Read-Host "Repository name (e.g., Auto-Punch-IDE-Releases)"
            $repoDesc = Read-Host "Description (optional)"
            
            Write-Host ""
            Write-Host "[~] Creating private repository..." -ForegroundColor Yellow
            if ($repoDesc) {
                gh repo create $repoName --private --description $repoDesc --clone
            } else {
                gh repo create $repoName --private --clone
            }
            
            if ($LASTEXITCODE -eq 0) {
                $repoPath = $repoName
                Write-Host "[+] Repository created and cloned" -ForegroundColor Green
            } else {
                Write-Host "[!] Failed to create repository" -ForegroundColor Red
                exit 1
            }
        } else {
            $repoOwner = Read-Host "Repository Owner/Username"
            $repoName = Read-Host "Repository Name"
            $repoPath = $repoName
            
            Write-Host ""
            Write-Host "[~] Cloning repository..." -ForegroundColor Yellow
            gh repo clone "$repoOwner/$repoName" $repoPath
            
            if ($LASTEXITCODE -ne 0) {
                Write-Host "[!] Failed to clone repository" -ForegroundColor Red
                exit 1
            }
            Write-Host "[+] Repository cloned" -ForegroundColor Green
        }
    } else {
        # Use Git directly
        Write-Host ""
        Write-Host "Using Git directly..." -ForegroundColor Yellow
        Write-Host "Note: You'll need to authenticate when pushing" -ForegroundColor Yellow
        Write-Host ""
        
        $repoOwner = Read-Host "Repository Owner/Username"
        $repoName = Read-Host "Repository Name"
        $repoPath = $repoName
        
        Write-Host ""
        Write-Host "[~] Cloning repository..." -ForegroundColor Yellow
        Write-Host "If prompted, use Personal Access Token as password" -ForegroundColor Yellow
        
        git clone "https://github.com/$repoOwner/$repoName.git" $repoPath 2>&1 | Out-Null
        
        if ($LASTEXITCODE -ne 0) {
            Write-Host "[!] Failed to clone. Check:" -ForegroundColor Red
            Write-Host "   - Repository exists and is accessible" -ForegroundColor White
            Write-Host "   - You have authentication set up" -ForegroundColor White
            Write-Host "   - For HTTPS: Use Personal Access Token" -ForegroundColor White
            Write-Host "   - For SSH: Use: git@github.com:$repoOwner/$repoName.git" -ForegroundColor White
            exit 1
        }
        Write-Host "[+] Repository cloned" -ForegroundColor Green
    }
} else {
    # Git only
    Write-Host "[!] GitHub CLI not found. Using Git directly." -ForegroundColor Yellow
    Write-Host "For easier authentication, install GitHub CLI: https://cli.github.com/" -ForegroundColor Yellow
    Write-Host ""
    
    $repoOwner = Read-Host "Repository Owner/Username"
    $repoName = Read-Host "Repository Name"
    $repoPath = $repoName
    
    Write-Host ""
    Write-Host "[~] Cloning repository..." -ForegroundColor Yellow
    Write-Host "If prompted, use Personal Access Token as password" -ForegroundColor Yellow
    
    git clone "https://github.com/$repoOwner/$repoName.git" $repoPath 2>&1 | Out-Null
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[!] Failed to clone. See CREATE_PRIVATE_REPO.md for authentication help" -ForegroundColor Red
        exit 1
    }
    Write-Host "[+] Repository cloned" -ForegroundColor Green
}

# Copy executable
Set-Location $repoPath

# Create releases directory
$releasesDir = "releases"
if (-not (Test-Path $releasesDir)) {
    New-Item -ItemType Directory -Path $releasesDir | Out-Null
}

# Copy executable
$exeName = Split-Path $exeFile -Leaf
$destPath = Join-Path $releasesDir $exeName
Copy-Item -Path (Resolve-Path "..\$exeFile") -Destination $destPath -Force
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

## Private Repository

This is a private repository for Auto_Punch IDE releases.
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
    
    Write-Host ""
    Write-Host "[~] Pushing to GitHub..." -ForegroundColor Yellow
    if ($ghAvailable -and ($useGH -eq "" -or $useGH -eq "Y" -or $useGH -eq "y")) {
        git push origin main 2>&1 | Out-Null
    } else {
        Write-Host "If prompted for credentials:" -ForegroundColor Yellow
        Write-Host "  Username: Your GitHub username" -ForegroundColor White
        Write-Host "  Password: Your Personal Access Token (not your password!)" -ForegroundColor White
        git push origin main
    }
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "============================================================" -ForegroundColor Green
        Write-Host "  SUCCESSFULLY UPLOADED TO PRIVATE REPOSITORY" -ForegroundColor Green
        Write-Host "============================================================" -ForegroundColor Green
        Write-Host ""
        Write-Host "Repository: https://github.com/$repoOwner/$repoName" -ForegroundColor Cyan
        Write-Host "File: releases/$exeName" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "Next: Create a GitHub Release for better distribution:" -ForegroundColor Yellow
        Write-Host "  https://github.com/$repoOwner/$repoName/releases/new" -ForegroundColor White
    } else {
        Write-Host ""
        Write-Host "[!] Push failed. Check authentication." -ForegroundColor Red
        Write-Host "See CREATE_PRIVATE_REPO.md for authentication help" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "File is ready at: $destPath" -ForegroundColor Cyan
        Write-Host "You can manually push or create a release via web interface" -ForegroundColor Yellow
    }
} else {
    Write-Host "[!] Commit failed" -ForegroundColor Red
    Write-Host "File is ready at: $destPath" -ForegroundColor Cyan
}

# Cleanup
Set-Location "C:\Users\Administrator\Auto_Punch IDE"
Write-Host ""
Write-Host "[~] Repository is at: $repoPath" -ForegroundColor Cyan
Write-Host "You can keep it for future updates or delete it" -ForegroundColor Yellow

Write-Host ""
Read-Host "Press Enter to exit"

