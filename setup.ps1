# Auto_Punch IDE - Setup Script
# Run this script to set up the desktop app development environment

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Auto_Punch IDE - Desktop App Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check Node.js
Write-Host "Checking Node.js..." -ForegroundColor Yellow
$nodeCheck = Get-Command node -ErrorAction SilentlyContinue
if ($nodeCheck) {
    $nodeVersion = node --version
    Write-Host "Node.js found: $nodeVersion" -ForegroundColor Green
} else {
    Write-Host "Node.js not found!" -ForegroundColor Red
    Write-Host "Please install Node.js 18+ from https://nodejs.org/" -ForegroundColor Red
    exit 1
}

# Check Python
Write-Host "Checking Python..." -ForegroundColor Yellow
$pythonCheck = Get-Command python -ErrorAction SilentlyContinue
if ($pythonCheck) {
    $pythonVersion = python --version
    Write-Host "Python found: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "Python not found!" -ForegroundColor Red
    Write-Host "Please install Python 3.8+ from https://www.python.org/" -ForegroundColor Red
    exit 1
}

# Check Git
Write-Host "Checking Git..." -ForegroundColor Yellow
$gitCheck = Get-Command git -ErrorAction SilentlyContinue
if ($gitCheck) {
    $gitVersion = git --version
    Write-Host "Git found: $gitVersion" -ForegroundColor Green
} else {
    Write-Host "Git not found!" -ForegroundColor Red
    Write-Host "Please install Git from https://git-scm.com/" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Installing Node.js dependencies..." -ForegroundColor Yellow
npm install
if ($LASTEXITCODE -ne 0) {
    Write-Host "Failed to install Node.js dependencies!" -ForegroundColor Red
    exit 1
}
Write-Host "Node.js dependencies installed" -ForegroundColor Green

Write-Host ""
Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "Failed to install Python dependencies!" -ForegroundColor Red
    exit 1
}
Write-Host "Python dependencies installed" -ForegroundColor Green

Write-Host ""
Write-Host "Checking for icons..." -ForegroundColor Yellow
if (Test-Path "resources\icon.ico") {
    Write-Host "Main icon found" -ForegroundColor Green
} else {
    Write-Host "Main icon missing (resources\icon.ico)" -ForegroundColor Yellow
    Write-Host "Create a 256x256 icon and save as resources\icon.ico" -ForegroundColor Yellow
}

if (Test-Path "resources\installer-icon.ico") {
    Write-Host "Installer icon found" -ForegroundColor Green
} else {
    Write-Host "Installer icon missing (resources\installer-icon.ico)" -ForegroundColor Yellow
    Write-Host "Create a 256x256 icon and save as resources\installer-icon.ico" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Create icons (if missing) and place in resources folder" -ForegroundColor White
Write-Host "2. Test development build: npm run dev" -ForegroundColor White
Write-Host "3. Build installers: npm run build:all" -ForegroundColor White
Write-Host ""
Write-Host "See QUICK_START.md for detailed instructions" -ForegroundColor Cyan
Write-Host ""
