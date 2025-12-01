# Auto_Punch IDE - Setup Verification Script
# Verifies all components are ready for desktop app build

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Auto_Punch IDE - Setup Verification" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$allGood = $true

# Check Python
Write-Host "Checking Python..." -ForegroundColor Yellow
$pythonCheck = Get-Command python -ErrorAction SilentlyContinue
if ($pythonCheck) {
    $pythonVersion = python --version
    Write-Host "  Python: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "  Python not found" -ForegroundColor Red
    $allGood = $false
}

# Check Python Dependencies
Write-Host "Checking Python dependencies..." -ForegroundColor Yellow
$flaskCheck = python -m pip show flask -ErrorAction SilentlyContinue
if ($flaskCheck) {
    Write-Host "  Flask installed" -ForegroundColor Green
} else {
    Write-Host "  Flask not installed" -ForegroundColor Red
    $allGood = $false
}

# Check Node.js
Write-Host "Checking Node.js..." -ForegroundColor Yellow
$nodeCheck = Get-Command node -ErrorAction SilentlyContinue
if ($nodeCheck) {
    $nodeVersion = node --version
    Write-Host "  Node.js: $nodeVersion" -ForegroundColor Green
} else {
    Write-Host "  Node.js not found (required for desktop app)" -ForegroundColor Red
    Write-Host "    Run: .\install-nodejs.ps1" -ForegroundColor Yellow
    $allGood = $false
}

# Check npm
if ($nodeCheck) {
    Write-Host "Checking npm..." -ForegroundColor Yellow
    $npmCheck = Get-Command npm -ErrorAction SilentlyContinue
    if ($npmCheck) {
        $npmVersion = npm --version
        Write-Host "  npm: $npmVersion" -ForegroundColor Green
        
        # Check if node_modules exists
        if (Test-Path "node_modules") {
            Write-Host "  Node.js dependencies installed" -ForegroundColor Green
        } else {
            Write-Host "  Node.js dependencies not installed" -ForegroundColor Yellow
            Write-Host "    Run: npm install" -ForegroundColor Yellow
        }
    }
}

# Check Git
Write-Host "Checking Git..." -ForegroundColor Yellow
$gitCheck = Get-Command git -ErrorAction SilentlyContinue
if ($gitCheck) {
    $gitVersion = git --version
    Write-Host "  Git: $gitVersion" -ForegroundColor Green
} else {
    Write-Host "  Git not found (optional)" -ForegroundColor Yellow
}

# Check Project Files
Write-Host "Checking project files..." -ForegroundColor Yellow
$requiredFiles = @(
    "package.json",
    "electron\main.js",
    "electron\preload.js",
    "app.py",
    "requirements.txt"
)

foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Host "  $file" -ForegroundColor Green
    } else {
        Write-Host "  $file missing" -ForegroundColor Red
        $allGood = $false
    }
}

# Check Icons
Write-Host "Checking icons..." -ForegroundColor Yellow
if (Test-Path "resources\icon.ico") {
    Write-Host "  Main icon found" -ForegroundColor Green
} else {
    Write-Host "  Main icon missing (optional)" -ForegroundColor Yellow
}

if (Test-Path "resources\installer-icon.ico") {
    Write-Host "  Installer icon found" -ForegroundColor Green
} else {
    Write-Host "  Installer icon missing (optional)" -ForegroundColor Yellow
}

# Check Backup
Write-Host "Checking backup..." -ForegroundColor Yellow
if (Test-Path "..\Auto_Punch IDE - BACKUP") {
    Write-Host "  Backup found" -ForegroundColor Green
} else {
    Write-Host "  Backup not found" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan

if ($allGood -and $nodeCheck -and (Test-Path "node_modules")) {
    Write-Host "ALL SYSTEMS READY!" -ForegroundColor Green
    Write-Host ""
    Write-Host "You can now:" -ForegroundColor Cyan
    Write-Host "  Test: npm run dev" -ForegroundColor White
    Write-Host "  Build: npm run build:all" -ForegroundColor White
} elseif ($allGood -and $nodeCheck) {
    Write-Host "ALMOST READY!" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Next step:" -ForegroundColor Cyan
    Write-Host "  Run: npm install" -ForegroundColor White
} elseif ($allGood) {
    Write-Host "READY (except Node.js)" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Next step:" -ForegroundColor Cyan
    Write-Host "  Install Node.js: .\install-nodejs.ps1" -ForegroundColor White
    Write-Host "  Or download from: https://nodejs.org/" -ForegroundColor White
} else {
    Write-Host "SETUP INCOMPLETE" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please fix the issues above." -ForegroundColor Yellow
}

Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
