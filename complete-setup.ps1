# Auto_Punch IDE - Complete Setup Script
# Runs all remaining setup steps automatically

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Auto_Punch IDE - Complete Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Refresh PATH
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

# Step 1: Verify Node.js
Write-Host "Step 1: Verifying Node.js..." -ForegroundColor Yellow
$nodeCheck = Get-Command node -ErrorAction SilentlyContinue
if (-not $nodeCheck) {
    Write-Host "Node.js not found. Installing..." -ForegroundColor Yellow
    .\install-nodejs.ps1
    Start-Sleep -Seconds 2
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
}

$nodeVersion = node --version
$npmVersion = npm --version
Write-Host "  Node.js: $nodeVersion" -ForegroundColor Green
Write-Host "  npm: $npmVersion" -ForegroundColor Green

# Step 2: Install Node.js dependencies
Write-Host ""
Write-Host "Step 2: Installing Node.js dependencies..." -ForegroundColor Yellow
Write-Host "This may take 5-10 minutes. Please wait..." -ForegroundColor Gray

if (Test-Path "node_modules") {
    Write-Host "  Node modules already exist. Skipping..." -ForegroundColor Yellow
} else {
    npm install
    if ($LASTEXITCODE -ne 0) {
        Write-Host "  Installation failed. Trying again..." -ForegroundColor Yellow
        npm install --force
    }
}

if (Test-Path "node_modules") {
    Write-Host "  Node.js dependencies installed!" -ForegroundColor Green
} else {
    Write-Host "  Installation may still be in progress." -ForegroundColor Yellow
    Write-Host "  Run 'npm install' manually if needed." -ForegroundColor Yellow
}

# Step 3: Verify setup
Write-Host ""
Write-Host "Step 3: Verifying setup..." -ForegroundColor Yellow
.\verify-setup.ps1

# Step 4: Test development build (optional)
Write-Host ""
Write-Host "Step 4: Ready to test!" -ForegroundColor Green
Write-Host ""
Write-Host "Next commands:" -ForegroundColor Cyan
Write-Host "  Test: npm run dev" -ForegroundColor White
Write-Host "  Build: npm run build:all" -ForegroundColor White
Write-Host ""


