# Stop All Interfering Processes
# Run: .\stop-all-processes.ps1

Write-Host ""
Write-Host "Stopping all interfering processes..." -ForegroundColor Yellow
Write-Host ""

# Stop Python processes
$pythonProcs = Get-Process | Where-Object {$_.ProcessName -eq "python" -or $_.ProcessName -eq "pythonw"}
if ($pythonProcs) {
    Write-Host "Stopping Python processes..." -ForegroundColor Yellow
    $pythonProcs | Stop-Process -Force -ErrorAction SilentlyContinue
    Write-Host "  Stopped $($pythonProcs.Count) Python process(es)" -ForegroundColor Green
} else {
    Write-Host "No Python processes running" -ForegroundColor Gray
}

# Stop Node processes (except electron-builder if building)
$nodeProcs = Get-Process | Where-Object {$_.ProcessName -eq "node"} | Where-Object {$_.MainWindowTitle -notlike "*electron-builder*"}
if ($nodeProcs) {
    Write-Host "Stopping Node processes..." -ForegroundColor Yellow
    $nodeProcs | Stop-Process -Force -ErrorAction SilentlyContinue
    Write-Host "  Stopped $($nodeProcs.Count) Node process(es)" -ForegroundColor Green
} else {
    Write-Host "No interfering Node processes" -ForegroundColor Gray
}

# Stop Flask if running
$flaskProcs = Get-Process | Where-Object {$_.CommandLine -like "*app.py*"} -ErrorAction SilentlyContinue
if ($flaskProcs) {
    $flaskProcs | Stop-Process -Force -ErrorAction SilentlyContinue
}

Write-Host ""
Write-Host "All interfering processes stopped!" -ForegroundColor Green
Write-Host "You can now run commands without cancellation." -ForegroundColor Cyan
Write-Host ""


