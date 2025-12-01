# Rebuild with toolkit fix
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  REBUILDING WITH TOOLKIT FIX" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Stop running processes
Write-Host "[~] Stopping running processes..." -ForegroundColor Yellow
Get-Process | Where-Object {$_.ProcessName -like "*Auto_Punch*"} | Stop-Process -Force -ErrorAction SilentlyContinue
Get-Process python -ErrorAction SilentlyContinue | Where-Object {$_.MainWindowTitle -like "*Flask*" -or $_.CommandLine -like "*app.py*"} | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2

# Navigate to project directory
Set-Location "C:\Users\Administrator\Auto_Punch IDE"

# Rebuild
Write-Host "[~] Building application..." -ForegroundColor Yellow
npm run build:exe

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "============================================================" -ForegroundColor Green
    Write-Host "  BUILD SUCCESSFUL!" -ForegroundColor Green
    Write-Host "============================================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "The toolkit fix has been applied." -ForegroundColor Green
    Write-Host "You can now test with: .\TEST_BUILD.ps1" -ForegroundColor Cyan
} else {
    Write-Host ""
    Write-Host "============================================================" -ForegroundColor Red
    Write-Host "  BUILD FAILED" -ForegroundColor Red
    Write-Host "============================================================" -ForegroundColor Red
}

Write-Host ""
Write-Host "Press Enter to exit..."
Read-Host

