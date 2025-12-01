# Stop all interfering processes
# Run: .\stop-all.ps1

Write-Host "Stopping Python/Flask processes..." -ForegroundColor Yellow

# Stop Python processes (Flask app)
Get-Process | Where-Object {$_.ProcessName -eq "python" -or $_.ProcessName -eq "pythonw"} | Stop-Process -Force -ErrorAction SilentlyContinue

# Stop Node processes (if any old builds)
Get-Process | Where-Object {$_.ProcessName -eq "node"} | Where-Object {$_.Path -notlike "*electron-builder*"} | Stop-Process -Force -ErrorAction SilentlyContinue

Write-Host "Processes stopped." -ForegroundColor Green
Write-Host ""
Write-Host "You can now run build commands without interference." -ForegroundColor Cyan


