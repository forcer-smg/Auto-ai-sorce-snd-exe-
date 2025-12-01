# ============================================================
# TEST BUILD - Run the built executable (PowerShell version)
# ============================================================

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  TESTING BUILT EXECUTABLE" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptPath

# Check if executable exists
$exePath = Join-Path $scriptPath "dist\win-unpacked\Auto_Punch IDE.exe"
if (-not (Test-Path $exePath)) {
    Write-Host "ERROR: Built executable not found!" -ForegroundColor Red
    Write-Host "Expected: $exePath" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Please run the build first:" -ForegroundColor Yellow
    Write-Host "  npm run build:exe" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "[+] Found executable: $exePath" -ForegroundColor Green
Write-Host ""
Write-Host "[~] Starting Auto_Punch IDE..." -ForegroundColor Yellow
Write-Host ""

# Run the executable
Start-Process -FilePath $exePath

Write-Host "[+] Application started!" -ForegroundColor Green
Write-Host ""
Write-Host "The IDE should open in a new window." -ForegroundColor Cyan
Write-Host "If it doesn't start, check:" -ForegroundColor Yellow
Write-Host "  1. Python is installed and in PATH" -ForegroundColor Yellow
Write-Host "  2. Flask dependencies are installed" -ForegroundColor Yellow
Write-Host "  3. Port 5001 is available" -ForegroundColor Yellow
Write-Host ""
Read-Host "Press Enter to exit"

