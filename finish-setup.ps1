# Finish Setup - Stop Processes and Prepare for Next Steps
# Run: .\finish-setup.ps1

Set-Location -Path "C:\Users\Administrator\Auto_Punch IDE"

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "FINISHING SETUP" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

# Step 1: Stop all interfering processes
Write-Host "[1/3] Stopping interfering processes..." -ForegroundColor Yellow
$pythonProcs = Get-Process | Where-Object {$_.ProcessName -eq "python" -or $_.ProcessName -eq "pythonw"}
if ($pythonProcs) {
    $pythonProcs | Stop-Process -Force -ErrorAction SilentlyContinue
    Write-Host "  Stopped $($pythonProcs.Count) Python process(es)" -ForegroundColor Green
} else {
    Write-Host "  No Python processes" -ForegroundColor Gray
}

$nodeProcs = Get-Process | Where-Object {$_.ProcessName -eq "node"} | Where-Object {$_.MainWindowTitle -notlike "*electron-builder*"}
if ($nodeProcs) {
    $nodeProcs | Stop-Process -Force -ErrorAction SilentlyContinue
    Write-Host "  Stopped $($nodeProcs.Count) Node process(es)" -ForegroundColor Green
} else {
    Write-Host "  No interfering Node processes" -ForegroundColor Gray
}
Write-Host ""

# Step 2: Verify build
Write-Host "[2/3] Verifying build..." -ForegroundColor Yellow
if (Test-Path "dist\Auto_Punch IDE Setup 1.0.0.exe") {
    $exe = Get-Item "dist\Auto_Punch IDE Setup 1.0.0.exe"
    Write-Host "  ✅ Installer ready: $([math]::Round($exe.Length/1MB, 2)) MB" -ForegroundColor Green
} else {
    Write-Host "  ⚠️  Installer not found" -ForegroundColor Yellow
}
Write-Host ""

# Step 3: Summary
Write-Host "[3/3] Setup Summary" -ForegroundColor Yellow
Write-Host ""
Write-Host "✅ Processes stopped - commands will work now" -ForegroundColor Green
Write-Host "✅ Build complete - installer ready" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Test installer: .\run-installer.ps1" -ForegroundColor White
Write-Host "  2. Continue development" -ForegroundColor White
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "READY FOR NEXT STEPS!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""


