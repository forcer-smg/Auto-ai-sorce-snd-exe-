# Test Local Setup
# Run: .\test-local-setup.ps1

Set-Location -Path "C:\Users\Administrator\Auto_Punch IDE"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "TESTING LOCAL SETUP" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$allGood = $true

# Test 1: Python
Write-Host "[1/5] Testing Python..." -ForegroundColor Yellow
try {
    $pythonVersion = & python --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  Python: $pythonVersion" -ForegroundColor Green
    } else {
        throw "Python not found"
    }
} catch {
    Write-Host "  ERROR: Python not found!" -ForegroundColor Red
    $allGood = $false
}
Write-Host ""

# Test 2: Flask
Write-Host "[2/5] Testing Flask..." -ForegroundColor Yellow
try {
    $flaskCheck = & python -c "import flask; print(flask.__version__)" 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  Flask: $flaskCheck" -ForegroundColor Green
    } else {
        Write-Host "  ERROR: Flask not installed" -ForegroundColor Red
        Write-Host "    Run: pip install -r requirements.txt" -ForegroundColor Yellow
        $allGood = $false
    }
} catch {
    Write-Host "  ERROR: Flask check failed" -ForegroundColor Red
    $allGood = $false
}
Write-Host ""

# Test 3: Files
Write-Host "[3/5] Testing files..." -ForegroundColor Yellow
$requiredFiles = @("app.py", "requirements.txt", "electron\main.js", "package.json")
foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Host "  $file - OK" -ForegroundColor Green
    } else {
        Write-Host "  $file - MISSING" -ForegroundColor Red
        $allGood = $false
    }
}
Write-Host ""

# Test 4: Port
Write-Host "[4/5] Testing port 5001..." -ForegroundColor Yellow
$portInUse = Get-NetTCPConnection -LocalPort 5001 -ErrorAction SilentlyContinue
if ($portInUse) {
    Write-Host "  WARNING: Port 5001 is in use" -ForegroundColor Yellow
    Write-Host "    This is OK if Flask is already running" -ForegroundColor Gray
} else {
    Write-Host "  Port 5001 is available" -ForegroundColor Green
}
Write-Host ""

# Test 5: Config
Write-Host "[5/5] Testing configuration..." -ForegroundColor Yellow
if (Test-Path "electron\config.json") {
    try {
        $configContent = Get-Content "electron\config.json" -Raw
        $config = $configContent | ConvertFrom-Json
        if ($config.useLocalServer) {
            Write-Host "  Using local server: $($config.serverUrl)" -ForegroundColor Green
        } else {
            Write-Host "  WARNING: Not using local server" -ForegroundColor Yellow
            Write-Host "    Server URL: $($config.serverUrl)" -ForegroundColor Gray
        }
    } catch {
        Write-Host "  WARNING: Could not parse config.json" -ForegroundColor Yellow
    }
} else {
    Write-Host "  WARNING: config.json not found (will use defaults)" -ForegroundColor Yellow
}
Write-Host ""

# Summary
Write-Host "========================================" -ForegroundColor Cyan
if ($allGood) {
    Write-Host "ALL TESTS PASSED!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Your local setup is ready!" -ForegroundColor Green
    Write-Host ""
    Write-Host "To start development:" -ForegroundColor Cyan
    Write-Host "  .\start-local-dev.ps1" -ForegroundColor White
} else {
    Write-Host "SOME ISSUES FOUND" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Please fix the issues above before continuing" -ForegroundColor Yellow
}
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
