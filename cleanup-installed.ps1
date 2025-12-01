# Cleanup Crashed/Installed Apps
# Run: .\cleanup-installed.ps1

Set-Location -Path "C:\Users\Administrator\Auto_Punch IDE"

Write-Host ""
Write-Host "========================================" -ForegroundColor Red
Write-Host "CLEANING UP CRASHED/INSTALLED APPS" -ForegroundColor Red
Write-Host "========================================" -ForegroundColor Red
Write-Host ""

# Step 1: Find installed locations
Write-Host "[1/5] Finding installed locations..." -ForegroundColor Yellow

$installLocations = @(
    "$env:ProgramFiles\Auto_Punch IDE",
    "${env:ProgramFiles(x86)}\Auto_Punch IDE",
    "$env:LOCALAPPDATA\Programs\Auto_Punch IDE",
    "$env:APPDATA\Auto_Punch IDE"
)

$foundInstalls = @()
foreach ($location in $installLocations) {
    if (Test-Path $location) {
        $foundInstalls += $location
        Write-Host "  Found: $location" -ForegroundColor Cyan
    }
}

if ($foundInstalls.Count -eq 0) {
    Write-Host "  No installed locations found" -ForegroundColor Gray
} else {
    Write-Host "  Found $($foundInstalls.Count) installation(s)" -ForegroundColor Yellow
}
Write-Host ""

# Step 2: Find running processes
Write-Host "[2/5] Finding running processes..." -ForegroundColor Yellow

$processes = Get-Process | Where-Object {
    $_.ProcessName -like "*Auto_Punch*" -or 
    $_.ProcessName -like "*AutoPunch*" -or
    $_.ProcessName -like "*autopunch*" -or
    $_.MainWindowTitle -like "*Auto_Punch*" -or
    $_.Path -like "*Auto_Punch*" -or
    ($_.ProcessName -eq "electron" -and $_.Path -like "*Auto_Punch*")
}

if ($processes) {
    Write-Host "  Found $($processes.Count) running process(es):" -ForegroundColor Cyan
    $processes | ForEach-Object {
        Write-Host "    $($_.ProcessName) (PID: $($_.Id)) - $($_.Path)" -ForegroundColor Gray
    }
} else {
    Write-Host "  No running processes found" -ForegroundColor Gray
}
Write-Host ""

# Step 3: Stop all processes
Write-Host "[3/5] Stopping all processes..." -ForegroundColor Yellow
if ($processes) {
    $processes | ForEach-Object {
        Write-Host "    Stopping: $($_.ProcessName) (PID: $($_.Id))" -ForegroundColor Gray
        Stop-Process -Id $_.Id -Force -ErrorAction SilentlyContinue
    }
    Start-Sleep -Seconds 2
    Write-Host "  All processes stopped" -ForegroundColor Green
} else {
    Write-Host "  No processes to stop" -ForegroundColor Gray
}
Write-Host ""

# Step 4: Uninstall from Programs
Write-Host "[4/5] Checking for uninstaller..." -ForegroundColor Yellow

$uninstallers = @(
    "$env:ProgramFiles\Auto_Punch IDE\uninstall.exe",
    "${env:ProgramFiles(x86)}\Auto_Punch IDE\uninstall.exe",
    "$env:LOCALAPPDATA\Programs\Auto_Punch IDE\uninstall.exe"
)

$foundUninstaller = $false
foreach ($uninstaller in $uninstallers) {
    if (Test-Path $uninstaller) {
        Write-Host "  Found uninstaller: $uninstaller" -ForegroundColor Cyan
        Write-Host "    Run this to uninstall properly:" -ForegroundColor Yellow
        Write-Host "      Start-Process '$uninstaller'" -ForegroundColor White
        $foundUninstaller = $true
    }
}

if (-not $foundUninstaller) {
    Write-Host "  No uninstaller found" -ForegroundColor Gray
}
Write-Host ""

# Step 5: Manual cleanup options
Write-Host "[5/5] Cleanup Summary" -ForegroundColor Yellow
Write-Host ""

if ($foundInstalls.Count -gt 0) {
    Write-Host "Installed locations found:" -ForegroundColor Yellow
    $foundInstalls | ForEach-Object {
        Write-Host "  - $_" -ForegroundColor White
    }
    Write-Host ""
    Write-Host "To remove manually:" -ForegroundColor Cyan
    Write-Host "  1. Close all Auto_Punch IDE windows" -ForegroundColor Gray
    Write-Host "  2. Run uninstaller if available" -ForegroundColor Gray
    Write-Host "  3. Or manually delete the folders above" -ForegroundColor Gray
} else {
    Write-Host "No installed locations found" -ForegroundColor Green
    Write-Host "App may not be installed, or installed in a different location" -ForegroundColor Gray
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "CLEANUP OPTIONS" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Option 1: Use uninstaller (if found above)" -ForegroundColor Yellow
Write-Host "Option 2: Manual deletion (after stopping processes)" -ForegroundColor Yellow
Write-Host "Option 3: Reinstall fresh (will overwrite)" -ForegroundColor Yellow
Write-Host ""
Write-Host "To reinstall fresh:" -ForegroundColor Cyan
Write-Host "  .\run-installer.ps1" -ForegroundColor White
Write-Host ""


