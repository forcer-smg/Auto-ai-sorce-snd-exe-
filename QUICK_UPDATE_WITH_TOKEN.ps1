# Quick Update with Token Authentication
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  QUICK UPDATE - Auto-ai-sorce-snd-exe" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

Set-Location "C:\Users\Administrator\Auto_Punch IDE"

# Check if git repo
if (-not (Test-Path ".git")) {
    Write-Host "[!] Not a git repository. Run UPLOAD_TO_REPO.ps1 first." -ForegroundColor Red
    exit 1
}

# Check if remote is set
$remoteUrl = git remote get-url origin 2>$null
if (-not $remoteUrl) {
    Write-Host "[!] No remote configured. Run UPLOAD_TO_REPO.ps1 first." -ForegroundColor Red
    exit 1
}

# Check if token is in URL
if ($remoteUrl -notmatch "://.*:.*@") {
    Write-Host "[~] Remote URL doesn't have token. Updating..." -ForegroundColor Yellow
    Write-Host ""
    
    $token = Read-Host "Enter your GitHub Personal Access Token" -AsSecureString
    $tokenPlain = [Runtime.InteropServices.Marshal]::PtrToStringAuto(
        [Runtime.InteropServices.Marshal]::SecureStringToBSTR($token)
    )
    
    if ([string]::IsNullOrWhiteSpace($tokenPlain)) {
        Write-Host "[!] Token is required" -ForegroundColor Red
        exit 1
    }
    
    $username = Read-Host "Enter your GitHub username (or press Enter for 'forcer-smg')"
    if ([string]::IsNullOrWhiteSpace($username)) {
        $username = "forcer-smg"
    }
    
    $authenticatedUrl = "https://${username}:${tokenPlain}@github.com/forcer-smg/Auto-ai-sorce-snd-exe-.git"
    git remote set-url origin $authenticatedUrl
    Write-Host "[+] Remote updated with token" -ForegroundColor Green
    $tokenPlain = $null
    $token = $null
}

# Pull latest changes
Write-Host ""
Write-Host "[~] Pulling latest changes..." -ForegroundColor Yellow
git pull origin main

if ($LASTEXITCODE -ne 0) {
    Write-Host "[!] Pull failed. Check your connection and authentication." -ForegroundColor Red
    exit 1
}

Write-Host "[+] Up to date" -ForegroundColor Green

# Show status
Write-Host ""
Write-Host "[~] Current status:" -ForegroundColor Yellow
git status --short

# Ask what to do
Write-Host ""
Write-Host "What would you like to do?" -ForegroundColor Cyan
Write-Host "1. Just commit and push current changes" -ForegroundColor White
Write-Host "2. Build new release and push" -ForegroundColor White
Write-Host "3. Build, update release, and push" -ForegroundColor White
Write-Host ""
$choice = Read-Host "Choose option (1/2/3)"

if ($choice -eq "2" -or $choice -eq "3") {
    Write-Host ""
    Write-Host "[~] Building executable..." -ForegroundColor Yellow
    npm run build:exe
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "[+] Build successful" -ForegroundColor Green
        
        if ($choice -eq "3") {
            # Copy to releases
            $exePath = "dist\Auto_Punch IDE Setup 1.0.0.exe"
            if (Test-Path $exePath) {
                if (-not (Test-Path "releases")) {
                    New-Item -ItemType Directory -Path "releases" | Out-Null
                }
                Copy-Item -Path $exePath -Destination "releases\Auto_Punch IDE Setup 1.0.0.exe" -Force
                Write-Host "[+] Copied EXE to releases folder" -ForegroundColor Green
            }
        }
    } else {
        Write-Host "[!] Build failed" -ForegroundColor Red
        exit 1
    }
}

# Stage changes
Write-Host ""
Write-Host "[~] Staging changes..." -ForegroundColor Yellow
git add .

# Show what will be committed
Write-Host ""
Write-Host "Changes to commit:" -ForegroundColor Cyan
git status --short

Write-Host ""
$commitMessage = Read-Host "Commit message (or press Enter for default)"
if ([string]::IsNullOrWhiteSpace($commitMessage)) {
    if ($choice -eq "3") {
        $commitMessage = "Update release - $(Get-Date -Format 'yyyy-MM-dd')"
    } elseif ($choice -eq "2") {
        $commitMessage = "Build update - $(Get-Date -Format 'yyyy-MM-dd')"
    } else {
        $commitMessage = "Update - $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
    }
}

Write-Host ""
Write-Host "[~] Committing..." -ForegroundColor Yellow
git commit -m $commitMessage

if ($LASTEXITCODE -eq 0) {
    Write-Host "[+] Committed" -ForegroundColor Green
    
    Write-Host ""
    Write-Host "[~] Pushing to GitHub..." -ForegroundColor Yellow
    $branch = git branch --show-current
    if (-not $branch) {
        $branch = "main"
    }
    
    git push origin $branch
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "============================================================" -ForegroundColor Green
        Write-Host "  SUCCESSFULLY UPDATED" -ForegroundColor Green
        Write-Host "============================================================" -ForegroundColor Green
        Write-Host ""
        Write-Host "Repository updated on GitHub!" -ForegroundColor Cyan
        Write-Host "https://github.com/forcer-smg/Auto-ai-sorce-snd-exe-" -ForegroundColor Cyan
    } else {
        Write-Host ""
        Write-Host "[!] Push failed. Check authentication." -ForegroundColor Red
    }
} else {
    Write-Host ""
    Write-Host "[!] Commit failed" -ForegroundColor Red
}

Write-Host ""
Read-Host "Press Enter to exit"

