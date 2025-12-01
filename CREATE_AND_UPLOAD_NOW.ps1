# Create Repository and Upload - Using Provided Token
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  CREATE REPOSITORY & UPLOAD" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

Set-Location "C:\Users\Administrator\Auto_Punch IDE"

$repoOwner = "forcer-smg"
$repoName = "Auto-ai-sorce-snd-exe-"
$token = "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"
$authenticatedUrl = "https://${repoOwner}:${token}@github.com/$repoOwner/$repoName.git"

# Create repository using GitHub API
Write-Host "[~] Creating repository..." -ForegroundColor Yellow

$headers = @{
    "Authorization" = "token $token"
    "Accept" = "application/vnd.github.v3+json"
}

$body = @{
    name = $repoName
    description = "Auto_Punch IDE Desktop - Source code and releases"
    private = $true
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "https://api.github.com/user/repos" -Method Post -Headers $headers -Body $body -ContentType "application/json"
    Write-Host "[+] Repository created successfully!" -ForegroundColor Green
    Write-Host "    URL: $($response.html_url)" -ForegroundColor Cyan
} catch {
    $statusCode = $_.Exception.Response.StatusCode.value__
    if ($statusCode -eq 422) {
        Write-Host "[+] Repository already exists (or name conflict)" -ForegroundColor Yellow
    } else {
        Write-Host "[!] Error creating repository: $_" -ForegroundColor Red
        Write-Host "    Status: $statusCode" -ForegroundColor Red
        exit 1
    }
}

# Configure Git
Write-Host ""
Write-Host "[~] Configuring Git..." -ForegroundColor Yellow

$isGitRepo = Test-Path ".git"
if (-not $isGitRepo) {
    git init
    Write-Host "[+] Git initialized" -ForegroundColor Green
}

# Set remote
$currentRemote = git remote get-url origin 2>$null
if ($currentRemote) {
    git remote set-url origin $authenticatedUrl
} else {
    git remote add origin $authenticatedUrl
}
Write-Host "[+] Remote configured" -ForegroundColor Green

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
git commit -m "Initial commit - Auto_Punch IDE v1.0.0 with full source code and EXE"

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
        Write-Host ""
        Write-Host "⚠️  SECURITY NOTE: Token is in this script file." -ForegroundColor Yellow
        Write-Host "    Consider removing it after first use for security." -ForegroundColor Yellow
    } else {
        Write-Host ""
        Write-Host "[!] Push failed. Check:" -ForegroundColor Red
        Write-Host "   - Repository exists" -ForegroundColor White
        Write-Host "   - Token has 'repo' scope" -ForegroundColor White
        Write-Host "   - You have access to the repository" -ForegroundColor White
    }
} else {
    Write-Host "[!] Commit failed" -ForegroundColor Red
}

Write-Host ""
Read-Host "Press Enter to exit"

