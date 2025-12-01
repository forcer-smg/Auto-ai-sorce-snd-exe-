# Auto-Run All - Complete Automation
# Run: .\auto-run-all.ps1

Set-Location -Path "C:\Users\Administrator\Auto_Punch IDE"

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "AUTO-RUN ALL - COMPLETE AUTOMATION" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

# Step 1: Stop all interfering processes
Write-Host "[1/5] Stopping interfering processes..." -ForegroundColor Yellow
taskkill /F /IM python.exe /T 2>$null | Out-Null
taskkill /F /IM pythonw.exe /T 2>$null | Out-Null
Get-Process node -ErrorAction SilentlyContinue | Where-Object {$_.MainWindowTitle -notlike "*electron*"} | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2
Write-Host "  ✓ Processes stopped" -ForegroundColor Green
Write-Host ""

# Step 2: Refresh PATH
Write-Host "[2/5] Refreshing environment..." -ForegroundColor Yellow
$machinePath = [System.Environment]::GetEnvironmentVariable("Path","Machine")
$userPath = [System.Environment]::GetEnvironmentVariable("Path","User")
$env:Path = $machinePath + ";" + $userPath
Write-Host "  ✓ PATH refreshed" -ForegroundColor Green
Write-Host ""

# Step 3: Verify Node.js
Write-Host "[3/5] Verifying Node.js..." -ForegroundColor Yellow
try {
    $nodeVersion = & node --version 2>&1
    $npmVersion = & npm --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✓ Node.js: $nodeVersion" -ForegroundColor Green
        Write-Host "  ✓ npm: $npmVersion" -ForegroundColor Green
    } else {
        throw "Node.js not found"
    }
} catch {
    Write-Host "  ✗ Node.js not found!" -ForegroundColor Red
    Write-Host "  Please install Node.js first." -ForegroundColor Red
    exit 1
}
Write-Host ""

# Step 4: Check build status
Write-Host "[4/5] Checking build status..." -ForegroundColor Yellow
$installerPath = "dist\Auto_Punch IDE Setup 1.0.0.exe"
$portablePath = "dist\win-unpacked\Auto_Punch IDE.exe"

if (Test-Path $installerPath) {
    $exe = Get-Item $installerPath
    Write-Host "  ✓ Installer found: $([math]::Round($exe.Length/1MB, 2)) MB" -ForegroundColor Green
    Write-Host "    Location: $($exe.FullName)" -ForegroundColor Gray
} else {
    Write-Host "  ⚠ Installer not found, building..." -ForegroundColor Yellow
    Write-Host "    This will take 10-15 minutes..." -ForegroundColor Gray
    Write-Host ""
    
    & npm run build:exe
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host ""
        Write-Host "  ✗ Build failed!" -ForegroundColor Red
        Write-Host "  Trying with --force..." -ForegroundColor Yellow
        & npm run build:exe -- --force
    }
    
    if (Test-Path $installerPath) {
        Write-Host ""
        Write-Host "  ✓ Build successful!" -ForegroundColor Green
    } else {
        Write-Host ""
        Write-Host "  ✗ Build failed. Check errors above." -ForegroundColor Red
        exit 1
    }
}

if (Test-Path $portablePath) {
    Write-Host "  ✓ Portable app ready" -ForegroundColor Green
}
Write-Host ""

# Step 5: Summary
Write-Host "[5/5] Final Summary" -ForegroundColor Yellow
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "✅ ALL STEPS COMPLETE!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

Write-Host "Installer Location:" -ForegroundColor Cyan
if (Test-Path $installerPath) {
    $exe = Get-Item $installerPath
    Write-Host "  $($exe.FullName)" -ForegroundColor White
    Write-Host "  Size: $([math]::Round($exe.Length/1MB, 2)) MB" -ForegroundColor Gray
    Write-Host "  Created: $($exe.LastWriteTime)" -ForegroundColor Gray
}

Write-Host ""
Write-Host "Portable App:" -ForegroundColor Cyan
if (Test-Path $portablePath) {
    Write-Host "  $portablePath" -ForegroundColor White
}

Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Cyan
Write-Host "  1. Test installer: .\run-installer.ps1" -ForegroundColor White
Write-Host "  2. Open folder: explorer dist" -ForegroundColor White
Write-Host "  3. Continue development" -ForegroundColor White
Write-Host ""

# Open dist folder
Write-Host "Opening dist folder..." -ForegroundColor Yellow
Start-Sleep -Seconds 1
explorer dist

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "READY FOR NEXT STEPS!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

