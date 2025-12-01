# ============================================================
# Stop Auto_Punch IDE
# ============================================================

Write-Host ""
Write-Host "Stopping Auto_Punch IDE..." -ForegroundColor Yellow
Write-Host ""

# Stop Electron processes
$electronProcesses = Get-Process | Where-Object {
    $_.ProcessName -like "*Auto_Punch*" -or 
    $_.ProcessName -like "*electron*"
}

if ($electronProcesses) {
    $electronProcesses | ForEach-Object {
        Write-Host "  Stopping: $($_.ProcessName) (PID: $($_.Id))" -ForegroundColor Gray
        Stop-Process -Id $_.Id -Force -ErrorAction SilentlyContinue
    }
    Write-Host "  [+] Electron processes stopped" -ForegroundColor Green
} else {
    Write-Host "  [+] No Electron processes found" -ForegroundColor Green
}

# Stop Python Flask processes
$pythonProcesses = Get-Process python -ErrorAction SilentlyContinue | Where-Object {
    $cmdLine = (Get-WmiObject Win32_Process -Filter "ProcessId = $($_.Id)").CommandLine
    $cmdLine -like "*app.py*"
}

if ($pythonProcesses) {
    $pythonProcesses | ForEach-Object {
        Write-Host "  Stopping: Python Flask (PID: $($_.Id))" -ForegroundColor Gray
        Stop-Process -Id $_.Id -Force -ErrorAction SilentlyContinue
    }
    Write-Host "  [+] Python Flask processes stopped" -ForegroundColor Green
} else {
    Write-Host "  [+] No Python Flask processes found" -ForegroundColor Green
}

Write-Host ""
Write-Host "All processes stopped!" -ForegroundColor Green
Write-Host ""

