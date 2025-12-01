# Close Auto_Punch IDE and Install
# Run: .\close-and-install.ps1

Set-Location -Path "C:\Users\Administrator\Auto_Punch IDE"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "CLOSING AUTO_PUNCH IDE AND INSTALLING" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Find and close all Auto_Punch IDE processes
Write-Host "[1/3] Closing Auto_Punch IDE processes..." -ForegroundColor Yellow

$processes = Get-Process | Where-Object {
    $_.ProcessName -like "*Auto_Punch*" -or 
    $_.ProcessName -like "*AutoPunch*" -or
    $_.ProcessName -like "*autopunch*" -or
    $_.MainWindowTitle -like "*Auto_Punch*" -or
    $_.Path -like "*Auto_Punch*"
}

if ($processes) {
    Write-Host "  Found $($processes.Count) process(es):" -ForegroundColor Cyan
    $processes | ForEach-Object {
        Write-Host "    Closing: $($_.ProcessName) (PID: $($_.Id))" -ForegroundColor Gray
        try {
            Stop-Process -Id $_.Id -Force -ErrorAction Stop
            Write-Host "      Closed successfully" -ForegroundColor Green
        } catch {
            Write-Host "      Force closing..." -ForegroundColor Yellow
            taskkill /F /PID $_.Id >nul 2>&1
        }
    }
} else {
    Write-Host "  No Auto_Punch IDE processes found" -ForegroundColor Gray
}

# Also check for Electron processes that might be the app
Write-Host ""
Write-Host "  Checking Electron processes..." -ForegroundColor Cyan
$electronProcs = Get-Process | Where-Object {
    $_.ProcessName -eq "electron" -and 
    ($_.Path -like "*Auto_Punch*" -or $_.MainWindowTitle -like "*Auto_Punch*")
}

if ($electronProcs) {
    $electronProcs | ForEach-Object {
        Write-Host "    Closing: Electron (PID: $($_.Id))" -ForegroundColor Gray
        Stop-Process -Id $_.Id -Force -ErrorAction SilentlyContinue
    }
}

# Wait for processes to fully close
Write-Host ""
Write-Host "  Waiting for processes to close..." -ForegroundColor Gray
Start-Sleep -Seconds 3

# Verify they're closed
$stillRunning = Get-Process | Where-Object {
    $_.ProcessName -like "*Auto_Punch*" -or 
    $_.ProcessName -like "*AutoPunch*" -or
    ($_.ProcessName -eq "electron" -and $_.Path -like "*Auto_Punch*")
}

if ($stillRunning) {
    Write-Host "  WARNING: Some processes still running, force killing..." -ForegroundColor Yellow
    $stillRunning | ForEach-Object {
        taskkill /F /PID $_.Id >nul 2>&1
    }
    Start-Sleep -Seconds 2
} else {
    Write-Host "  All processes closed" -ForegroundColor Green
}

Write-Host ""

# Step 2: Verify installer exists
Write-Host "[2/3] Verifying installer..." -ForegroundColor Yellow
$installerPath = "dist\Auto_Punch IDE Setup 1.0.0.exe"

if (-not (Test-Path $installerPath)) {
    Write-Host "  ERROR: Installer not found!" -ForegroundColor Red
    Write-Host "  Location: $installerPath" -ForegroundColor Yellow
    Write-Host "  Please build the installer first." -ForegroundColor Red
    exit 1
}

$exe = Get-Item $installerPath
Write-Host "  Installer found: $([math]::Round($exe.Length/1MB, 2)) MB" -ForegroundColor Green
Write-Host ""

# Step 3: Run installer
Write-Host "[3/3] Running installer..." -ForegroundColor Yellow
Write-Host "  Starting installer..." -ForegroundColor Gray
Write-Host ""

try {
    Start-Process -FilePath $installerPath -Wait -ErrorAction Stop
    Write-Host ""
    Write-Host "  Installer completed!" -ForegroundColor Green
} catch {
    Write-Host ""
    Write-Host "  ERROR: Failed to run installer" -ForegroundColor Red
    Write-Host "  Error: $_" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "INSTALLATION COMPLETE!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""


