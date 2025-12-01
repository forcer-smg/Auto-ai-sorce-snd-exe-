# Start Local Development Server
# Run: .\start-local-dev.ps1

Set-Location -Path "C:\Users\Administrator\Auto_Punch IDE"

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "STARTING LOCAL DEVELOPMENT SERVER" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

# Check Python
Write-Host "[1/4] Checking Python..." -ForegroundColor Yellow
try {
    $pythonVersion = & python --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  Python: $pythonVersion" -ForegroundColor Green
    } else {
        throw "Python not found"
    }
} catch {
    Write-Host "  ERROR: Python not found!" -ForegroundColor Red
    Write-Host "  Please install Python 3.11+ from https://www.python.org/downloads/" -ForegroundColor Yellow
    exit 1
}
Write-Host ""

# Check dependencies
Write-Host "[2/4] Checking dependencies..." -ForegroundColor Yellow
if (Test-Path "requirements.txt") {
    Write-Host "  requirements.txt found" -ForegroundColor Green
    
    # Check if Flask is installed
    $flaskCheck = & python -c "import flask" 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Host "  Installing dependencies..." -ForegroundColor Yellow
        & pip install -r requirements.txt
        if ($LASTEXITCODE -ne 0) {
            Write-Host "  WARNING: Some dependencies may have failed to install" -ForegroundColor Yellow
        } else {
            Write-Host "  Dependencies installed" -ForegroundColor Green
        }
    } else {
        Write-Host "  Dependencies OK" -ForegroundColor Green
    }
} else {
    Write-Host "  WARNING: requirements.txt not found" -ForegroundColor Yellow
}
Write-Host ""

# Check port availability
Write-Host "[3/4] Checking port 5001..." -ForegroundColor Yellow
$portInUse = Get-NetTCPConnection -LocalPort 5001 -ErrorAction SilentlyContinue
if ($portInUse) {
    Write-Host "  WARNING: Port 5001 is in use!" -ForegroundColor Yellow
    Write-Host "  Process: $($portInUse.OwningProcess)" -ForegroundColor Gray
    Write-Host "  You may need to stop the existing Flask server" -ForegroundColor Yellow
} else {
    Write-Host "  Port 5001 is available" -ForegroundColor Green
}
Write-Host ""

# Start Flask server
Write-Host "[4/4] Starting Flask server..." -ForegroundColor Yellow
Write-Host ""
Write-Host "Server will start on: http://localhost:5001" -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Gray
Write-Host ""

# Start Flask directly (not in background job to avoid issues)
Write-Host "Starting Flask..." -ForegroundColor Green
Write-Host ""

# Run Flask directly
& python app.py
