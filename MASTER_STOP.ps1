# MASTER STOP SCRIPT - Run this first!
# This will stop ALL interfering processes

Write-Host ""
Write-Host "========================================" -ForegroundColor Red
Write-Host "STOPPING ALL INTERFERING PROCESSES" -ForegroundColor Red
Write-Host "========================================" -ForegroundColor Red
Write-Host ""

# Force stop Python
Write-Host "Stopping Python processes..." -ForegroundColor Yellow
taskkill /F /IM python.exe /T 2>$null
taskkill /F /IM pythonw.exe /T 2>$null
Start-Sleep -Seconds 1

# Force stop Node (except if building)
Write-Host "Stopping Node processes..." -ForegroundColor Yellow
Get-Process node -ErrorAction SilentlyContinue | Where-Object {$_.MainWindowTitle -notlike "*electron*"} | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 1

# Force stop Flask
Write-Host "Stopping Flask processes..." -ForegroundColor Yellow
Get-Process | Where-Object {$_.CommandLine -like "*app.py*"} -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "ALL PROCESSES STOPPED!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "You can now run commands without cancellation." -ForegroundColor Cyan
Write-Host ""


