# ============================================================
# Quick Rebuild - Just rebuild the app
# ============================================================

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  REBUILDING APPLICATION" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptPath

# Close running processes
Write-Host "[1/3] Closing running processes..." -ForegroundColor Yellow
Get-Process | Where-Object {
    $_.ProcessName -like "*Auto_Punch*" -or 
    $_.ProcessName -like "*electron*"
} | Stop-Process -Force -ErrorAction SilentlyContinue

Get-Process python -ErrorAction SilentlyContinue | Where-Object {
    $cmdLine = (Get-WmiObject Win32_Process -Filter "ProcessId = $($_.Id)").CommandLine
    $cmdLine -like "*app.py*"
} | Stop-Process -Force -ErrorAction SilentlyContinue

Start-Sleep -Seconds 2
Write-Host "[+] Processes closed" -ForegroundColor Green

# Rebuild
Write-Host ""
Write-Host "[2/3] Rebuilding application..." -ForegroundColor Yellow
Write-Host ""

npm run build:exe

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "[3/3] Build complete!" -ForegroundColor Green
    Write-Host ""
    Write-Host "============================================================" -ForegroundColor Green
    Write-Host "  BUILD SUCCESSFUL!" -ForegroundColor Green
    Write-Host "============================================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "The toolkit fix is now included!" -ForegroundColor Cyan
    Write-Host "New tools (365-Stealer, requests-ip-rotator) will now appear." -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Test with:" -ForegroundColor Yellow
    Write-Host "  .\TEST_BUILD.ps1" -ForegroundColor Cyan
} else {
    Write-Host ""
    Write-Host "============================================================" -ForegroundColor Red
    Write-Host "  BUILD FAILED" -ForegroundColor Red
    Write-Host "============================================================" -ForegroundColor Red
}

Write-Host ""
Read-Host "Press Enter to exit"

