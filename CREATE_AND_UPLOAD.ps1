# Create Repository and Upload Full Project
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  CREATE REPOSITORY & UPLOAD" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

Set-Location "C:\Users\Administrator\Auto_Punch IDE"

$repoOwner = "forcer-smg"
$repoName = "Auto-ai-sorce-snd-exe-"
$repoUrl = "https://github.com/$repoOwner/$repoName.git"

# Check GitHub CLI
$ghAvailable = Get-Command gh -ErrorAction SilentlyContinue

if ($ghAvailable) {
    Write-Host "[+] GitHub CLI found" -ForegroundColor Green
    
    # Check authentication
    Write-Host ""
    Write-Host "[~] Checking GitHub CLI authentication..." -ForegroundColor Yellow
    $authStatus = gh auth status 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[!] Not authenticated. Starting authentication..." -ForegroundColor Yellow
        gh auth login
    } else {
        Write-Host "[+] Authenticated with GitHub CLI" -ForegroundColor Green
    }
    
    # Check if repo exists
    Write-Host ""
    Write-Host "[~] Checking if repository exists..." -ForegroundColor Yellow
    $repoExists = gh repo view "$repoOwner/$repoName" 2>&1
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[!] Repository doesn't exist. Creating..." -ForegroundColor Yellow
        Write-Host ""
        
        $repoDesc = Read-Host "Repository description (or press Enter for default)"
        if ([string]::IsNullOrWhiteSpace($repoDesc)) {
            $repoDesc = "Auto_Punch IDE Desktop - Source code and releases"
        }
        
        Write-Host ""
        Write-Host "[~] Creating private repository..." -ForegroundColor Yellow
        gh repo create $repoName --private --description $repoDesc
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "[+] Repository created successfully!" -ForegroundColor Green
        } else {
            Write-Host "[!] Failed to create repository" -ForegroundColor Red
            Write-Host ""
            Write-Host "Please create it manually:" -ForegroundColor Yellow
            Write-Host "1. Go to: https://github.com/new" -ForegroundColor White
            Write-Host "2. Repository name: $repoName" -ForegroundColor White
            Write-Host "3. Select: Private" -ForegroundColor White
            Write-Host "4. Click 'Create repository'" -ForegroundColor White
            exit 1
        }
    } else {
        Write-Host "[+] Repository already exists" -ForegroundColor Green
    }
} else {
    Write-Host "[!] GitHub CLI not found" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Please create the repository manually:" -ForegroundColor Yellow
    Write-Host "1. Go to: https://github.com/new" -ForegroundColor White
    Write-Host "2. Repository name: $repoName" -ForegroundColor White
    Write-Host "3. Select: Private" -ForegroundColor White
    Write-Host "4. Click 'Create repository'" -ForegroundColor White
    Write-Host ""
    $created = Read-Host "Have you created the repository? (Y/n)"
    
    if ($created -ne "Y" -and $created -ne "y") {
        Write-Host "[!] Please create the repository first" -ForegroundColor Red
        exit 1
    }
}

# Now run the upload script
Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host "  REPOSITORY READY - STARTING UPLOAD" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""

# Get token
Write-Host "Enter your GitHub Personal Access Token:" -ForegroundColor Yellow
Write-Host "(If you don't have one, get it from: https://github.com/settings/tokens)" -ForegroundColor Gray
Write-Host ""
$token = Read-Host "Token" -AsSecureString
$tokenPlain = [Runtime.InteropServices.Marshal]::PtrToStringAuto(
    [Runtime.InteropServices.Marshal]::SecureStringToBSTR($token)
)

if ([string]::IsNullOrWhiteSpace($tokenPlain)) {
    Write-Host "[!] Token is required" -ForegroundColor Red
    exit 1
}

# Configure Git
Write-Host ""
Write-Host "[~] Configuring Git..." -ForegroundColor Yellow

$username = Read-Host "Enter your GitHub username (or press Enter for '$repoOwner')"
if ([string]::IsNullOrWhiteSpace($username)) {
    $username = $repoOwner
}

$authenticatedUrl = "https://${username}:${tokenPlain}@github.com/$repoOwner/$repoName.git"

# Check if git repo
$isGitRepo = Test-Path ".git"
if (-not $isGitRepo) {
    git init
}

# Set remote
$currentRemote = git remote get-url origin 2>$null
if ($currentRemote) {
    git remote set-url origin $authenticatedUrl
} else {
    git remote add origin $authenticatedUrl
}

Write-Host "[+] Git configured" -ForegroundColor Green

# Update .gitignore
Write-Host ""
Write-Host "[~] Updating .gitignore..." -ForegroundColor Yellow
$gitignoreContent = Get-Content .gitignore -Raw -ErrorAction SilentlyContinue
if (-not $gitignoreContent) {
    $gitignoreContent = ""
}
if ($gitignoreContent -notmatch "!releases/") {
    $gitignoreContent += "`n# Allow releases folder`n!releases/`n!releases/**/*.exe`n"
    Set-Content -Path ".gitignore" -Value $gitignoreContent
}

# Prepare releases
Write-Host ""
Write-Host "[~] Preparing releases..." -ForegroundColor Yellow
$releasesDir = "releases"
if (-not (Test-Path $releasesDir)) {
    New-Item -ItemType Directory -Path $releasesDir | Out-Null
}

$exePath = "dist\Auto_Punch IDE Setup 1.0.0.exe"
if (Test-Path $exePath) {
    Copy-Item -Path $exePath -Destination "$releasesDir\Auto_Punch IDE Setup 1.0.0.exe" -Force
    Write-Host "[+] EXE copied to releases" -ForegroundColor Green
}

# Stage and commit
Write-Host ""
Write-Host "[~] Staging files..." -ForegroundColor Yellow
git add .

Write-Host ""
Write-Host "[~] Committing..." -ForegroundColor Yellow
$commitMessage = Read-Host "Commit message (or press Enter for default)"
if ([string]::IsNullOrWhiteSpace($commitMessage)) {
    $commitMessage = "Initial commit - Auto_Punch IDE v1.0.0 with full source code and EXE"
}

git commit -m $commitMessage

if ($LASTEXITCODE -eq 0) {
    Write-Host "[+] Committed" -ForegroundColor Green
    
    Write-Host ""
    Write-Host "[~] Pushing to GitHub..." -ForegroundColor Yellow
    
    $branch = git branch --show-current
    if (-not $branch) {
        $branch = "main"
        git branch -M main
    }
    
    git push -u origin $branch
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "============================================================" -ForegroundColor Green
        Write-Host "  SUCCESSFULLY UPLOADED!" -ForegroundColor Green
        Write-Host "============================================================" -ForegroundColor Green
        Write-Host ""
        Write-Host "Repository: https://github.com/$repoOwner/$repoName" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "✅ Repository created" -ForegroundColor Green
        Write-Host "✅ Full source code uploaded" -ForegroundColor Green
        Write-Host "✅ EXE uploaded to releases folder" -ForegroundColor Green
    } else {
        Write-Host ""
        Write-Host "[!] Push failed. Check token and repository access." -ForegroundColor Red
    }
} else {
    Write-Host "[!] Commit failed" -ForegroundColor Red
}

# Clear token
$tokenPlain = $null
$token = $null

Write-Host ""
Read-Host "Press Enter to exit"

