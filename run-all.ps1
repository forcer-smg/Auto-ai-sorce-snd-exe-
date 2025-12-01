# Auto_Punch IDE - Complete Auto-Run Script
# This script completes all remaining setup steps

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Auto_Punch IDE - Complete Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Refresh PATH
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

# Step 1: Verify Node.js
Write-Host "[1/4] Checking Node.js..." -ForegroundColor Yellow
$nodeCheck = Get-Command node -ErrorAction SilentlyContinue
if ($nodeCheck) {
    $nodeVersion = node --version
    $npmVersion = npm --version
    Write-Host "  Node.js: $nodeVersion" -ForegroundColor Green
    Write-Host "  npm: $npmVersion" -ForegroundColor Green
} else {
    Write-Host "  Node.js not found. Installing..." -ForegroundColor Yellow
    .\install-nodejs.ps1
    Start-Sleep -Seconds 3
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
}

# Step 2: Install npm dependencies
Write-Host ""
Write-Host "[2/4] Installing npm dependencies..." -ForegroundColor Yellow
Write-Host "  This will take 5-10 minutes..." -ForegroundColor Gray

if (Test-Path "node_modules\electron") {
    Write-Host "  Dependencies already installed!" -ForegroundColor Green
} else {
    npm install
    if ($LASTEXITCODE -ne 0) {
        Write-Host "  Retrying installation..." -ForegroundColor Yellow
        npm install --force
    }
    
    if (Test-Path "node_modules\electron") {
        Write-Host "  Dependencies installed successfully!" -ForegroundColor Green
    } else {
        Write-Host "  Installation may have issues. Check manually." -ForegroundColor Yellow
        exit 1
    }
}

# Step 3: Verify setup
Write-Host ""
Write-Host "[3/4] Verifying setup..." -ForegroundColor Yellow
if (Test-Path "node_modules\electron") {
    Write-Host "  Electron: Ready" -ForegroundColor Green
} else {
    Write-Host "  Electron: Missing" -ForegroundColor Red
}

if (Test-Path "node_modules\electron-builder") {
    Write-Host "  electron-builder: Ready" -ForegroundColor Green
} else {
    Write-Host "  electron-builder: Missing" -ForegroundColor Red
}

# Step 4: Build installers
Write-Host ""
Write-Host "[4/4] Building installers..." -ForegroundColor Yellow
Write-Host "  This will take 10-15 minutes..." -ForegroundColor Gray
Write-Host "  Creating both MSI and EXE installers..." -ForegroundColor Gray

npm run build:all

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "BUILD COMPLETE!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Installers created in dist/ folder:" -ForegroundColor Cyan
    if (Test-Path "dist\*.msi") {
        Get-ChildItem "dist\*.msi" | ForEach-Object { Write-Host "  MSI: $($_.Name)" -ForegroundColor Green }
    }
    if (Test-Path "dist\*.exe") {
        Get-ChildItem "dist\*.exe" | ForEach-Object { Write-Host "  EXE: $($_.Name)" -ForegroundColor Green }
    }
    Write-Host ""
    Write-Host "You can now distribute these installers!" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "Build had issues. Check errors above." -ForegroundColor Yellow
    Write-Host "You can try: npm run build:all" -ForegroundColor Yellow
}

Write-Host ""


