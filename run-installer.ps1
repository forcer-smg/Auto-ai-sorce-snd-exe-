# Run the Installer (Closes running instances first)
# Run: .\run-installer.ps1

Set-Location -Path "C:\Users\Administrator\Auto_Punch IDE"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "INSTALLING AUTO_PUNCH IDE" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Close any running instances
Write-Host "[1/2] Closing running Auto_Punch IDE instances..." -ForegroundColor Yellow

$processes = Get-Process | Where-Object {
    $_.ProcessName -like "*Auto_Punch*" -or 
    $_.ProcessName -like "*AutoPunch*" -or
    $_.ProcessName -like "*autopunch*" -or
    $_.MainWindowTitle -like "*Auto_Punch*" -or
    $_.Path -like "*Auto_Punch*" -or
    ($_.ProcessName -eq "electron" -and $_.Path -like "*Auto_Punch*")
}

if ($processes) {
    Write-Host "  Found $($processes.Count) process(es), closing..." -ForegroundColor Cyan
    $processes | ForEach-Object {
        Write-Host "    Closing: $($_.ProcessName) (PID: $($_.Id))" -ForegroundColor Gray
        Stop-Process -Id $_.Id -Force -ErrorAction SilentlyContinue
    }
    Start-Sleep -Seconds 3
    Write-Host "  All processes closed" -ForegroundColor Green
} else {
    Write-Host "  No running instances found" -ForegroundColor Gray
}
Write-Host ""

# Step 2: Run installer
Write-Host "[2/2] Running installer..." -ForegroundColor Yellow
$installerPath = "dist\Auto_Punch IDE Setup 1.0.0.exe"

if (Test-Path $installerPath) {
    Write-Host "  Launching installer..." -ForegroundColor Gray
    Write-Host ""
    
    try {
        Start-Process -FilePath $installerPath -Wait -ErrorAction Stop
        Write-Host ""
        Write-Host "  Installer completed successfully!" -ForegroundColor Green
    } catch {
        Write-Host ""
        Write-Host "  ERROR: Failed to run installer" -ForegroundColor Red
        Write-Host "  Error: $_" -ForegroundColor Yellow
        exit 1
    }
} else {
    Write-Host ""
    Write-Host "  ERROR: Installer not found!" -ForegroundColor Red
    Write-Host "  Expected: $installerPath" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "  Run build first:" -ForegroundColor Cyan
    Write-Host "    .\WORKING_RUN_ALL.bat" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "INSTALLATION COMPLETE!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
