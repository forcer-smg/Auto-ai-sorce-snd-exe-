# ============================================================
# CLEAN REBUILD - Close running processes and rebuild
# ============================================================

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  CLEANING UP AND REBUILDING" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptPath

# Step 1: Close Auto_Punch IDE processes
Write-Host "[1/4] Closing Auto_Punch IDE processes..." -ForegroundColor Yellow
try {
    $processes = Get-Process | Where-Object {
        $_.ProcessName -like "*Auto_Punch*" -or 
        $_.ProcessName -like "*electron*" -or
        ($_.MainWindowTitle -like "*Auto_Punch*" -and $_.MainWindowTitle -ne "")
    }
    
    if ($processes) {
        $processes | ForEach-Object {
            Write-Host "  Closing: $($_.ProcessName) (PID: $($_.Id))" -ForegroundColor Gray
            Stop-Process -Id $_.Id -Force -ErrorAction SilentlyContinue
        }
        Write-Host "[+] Processes closed" -ForegroundColor Green
    } else {
        Write-Host "[+] No Auto_Punch IDE processes found" -ForegroundColor Green
    }
} catch {
    Write-Host "[!] Error closing processes: $_" -ForegroundColor Red
}

# Step 2: Close Python Flask processes
Write-Host ""
Write-Host "[2/4] Closing Python Flask processes..." -ForegroundColor Yellow
try {
    $pythonProcesses = Get-Process python -ErrorAction SilentlyContinue | Where-Object {
        $_.Path -like "*Python*" -and 
        (Get-WmiObject Win32_Process -Filter "ProcessId = $($_.Id)").CommandLine -like "*app.py*"
    }
    
    if ($pythonProcesses) {
        $pythonProcesses | ForEach-Object {
            Write-Host "  Closing: Python (PID: $($_.Id))" -ForegroundColor Gray
            Stop-Process -Id $_.Id -Force -ErrorAction SilentlyContinue
        }
        Write-Host "[+] Python processes closed" -ForegroundColor Green
    } else {
        Write-Host "[+] No Python Flask processes found" -ForegroundColor Green
    }
} catch {
    Write-Host "[!] Error closing Python processes: $_" -ForegroundColor Red
}

# Step 3: Wait a moment for processes to fully close
Write-Host ""
Write-Host "[3/4] Waiting for processes to close..." -ForegroundColor Yellow
Start-Sleep -Seconds 3
Write-Host "[+] Ready" -ForegroundColor Green

# Step 4: Rebuild
Write-Host ""
Write-Host "[4/4] Rebuilding application..." -ForegroundColor Yellow
Write-Host ""

try {
    npm run build:exe
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "============================================================" -ForegroundColor Green
        Write-Host "  BUILD SUCCESSFUL!" -ForegroundColor Green
        Write-Host "============================================================" -ForegroundColor Green
        Write-Host ""
        Write-Host "You can now test the build with:" -ForegroundColor Cyan
        Write-Host "  .\TEST_BUILD.ps1" -ForegroundColor Yellow
    } else {
        Write-Host ""
        Write-Host "============================================================" -ForegroundColor Red
        Write-Host "  BUILD FAILED" -ForegroundColor Red
        Write-Host "============================================================" -ForegroundColor Red
    }
} catch {
    Write-Host ""
    Write-Host "[!] Build error: $_" -ForegroundColor Red
}

Write-Host ""
Read-Host "Press Enter to exit"

