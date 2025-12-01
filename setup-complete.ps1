# Auto_Punch IDE - Complete Setup Script
# Run: .\setup-complete.ps1

# Refresh PATH to ensure npm is available
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "Auto_Punch IDE - Complete Setup" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

# Change to project directory
Set-Location -Path "C:\Users\Administrator\Auto_Punch IDE"

# Step 1: Verify Node.js and npm
Write-Host "[1/4] Verifying Node.js..." -ForegroundColor Yellow
try {
    $nodeVersion = & node --version 2>&1
    $npmVersion = & npm --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  Node.js: $nodeVersion" -ForegroundColor Green
        Write-Host "  npm: $npmVersion" -ForegroundColor Green
    } else {
        throw "Node.js not found"
    }
} catch {
    Write-Host "  ERROR: Node.js or npm not found!" -ForegroundColor Red
    Write-Host "  Please install Node.js first." -ForegroundColor Red
    exit 1
}
Write-Host ""

# Step 2: Install npm dependencies
Write-Host "[2/4] Installing npm dependencies..." -ForegroundColor Yellow
Write-Host "  This will take 5-10 minutes. Please wait..." -ForegroundColor Gray
Write-Host ""

& npm install

if ($LASTEXITCODE -ne 0) {
    Write-Host "  WARNING: npm install had issues. Trying with --force..." -ForegroundColor Yellow
    & npm install --force
}

Write-Host ""
Write-Host "  Checking installation..." -ForegroundColor Gray
if (Test-Path "node_modules\electron") {
    Write-Host "  [OK] Electron: Installed" -ForegroundColor Green
} else {
    Write-Host "  [FAIL] Electron: Missing" -ForegroundColor Red
}

if (Test-Path "node_modules\electron-builder") {
    Write-Host "  [OK] electron-builder: Installed" -ForegroundColor Green
} else {
    Write-Host "  [FAIL] electron-builder: Missing" -ForegroundColor Red
}
Write-Host ""

# Step 3: Verify installation
Write-Host "[3/4] Verifying installation..." -ForegroundColor Yellow
if (-not (Test-Path "node_modules\electron")) {
    Write-Host "  ERROR: Critical dependencies missing!" -ForegroundColor Red
    Write-Host "  Please run 'npm install' manually and check for errors." -ForegroundColor Red
    exit 1
}
Write-Host "  [OK] All dependencies ready" -ForegroundColor Green
Write-Host ""

# Step 4: Build installers
Write-Host "[4/4] Building installers..." -ForegroundColor Yellow
Write-Host "  This will take 10-15 minutes. Please wait..." -ForegroundColor Gray
Write-Host ""

& npm run build:all

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "  ERROR: Build failed. Check errors above." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "BUILD COMPLETE!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

# List created installers
Write-Host "Installers created in dist\ folder:" -ForegroundColor Cyan
Write-Host ""

if (Test-Path "dist\*.msi") {
    Get-ChildItem "dist\*.msi" | ForEach-Object {
        Write-Host "  MSI: $($_.Name)" -ForegroundColor Green
    }
}

if (Test-Path "dist\*.exe") {
    Get-ChildItem "dist\*.exe" | ForEach-Object {
        Write-Host "  EXE: $($_.Name)" -ForegroundColor Green
    }
}

if (Test-Path "dist\win-unpacked\Auto_Punch IDE.exe") {
    Write-Host "  Portable: win-unpacked\Auto_Punch IDE.exe" -ForegroundColor Green
}

Write-Host ""
Write-Host "Setup complete! You can now distribute the installers." -ForegroundColor Green
Write-Host ""


