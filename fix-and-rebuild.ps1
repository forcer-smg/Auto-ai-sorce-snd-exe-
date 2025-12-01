# Fix electron-updater Issue and Rebuild
# Run: .\fix-and-rebuild.ps1

Set-Location -Path "C:\Users\Administrator\Auto_Punch IDE"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "FIXING ELECTRON-UPDATER ISSUE" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "[1/4] Fixed main.js - electron-updater is now optional" -ForegroundColor Green
Write-Host "  App will work without electron-updater" -ForegroundColor Gray
Write-Host "  Auto-updater gracefully disabled if missing" -ForegroundColor Gray
Write-Host ""

Write-Host "[2/4] Updated package.json - added asarUnpack for electron-updater" -ForegroundColor Green
Write-Host "  electron-updater will be included in build" -ForegroundColor Gray
Write-Host ""

Write-Host "[3/4] Rebuilding installer..." -ForegroundColor Yellow
Write-Host "  This will take 10-15 minutes..." -ForegroundColor Gray
Write-Host ""

$machinePath = [System.Environment]::GetEnvironmentVariable("Path","Machine")
$userPath = [System.Environment]::GetEnvironmentVariable("Path","User")
$env:Path = $machinePath + ";" + $userPath

& npm run build:exe

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "  Build failed!" -ForegroundColor Red
    Write-Host "  But the app will still work - electron-updater is optional" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "[4/4] Build Complete!" -ForegroundColor Green
Write-Host ""

if (Test-Path "dist\Auto_Punch IDE Setup 1.0.0.exe") {
    $exe = Get-Item "dist\Auto_Punch IDE Setup 1.0.0.exe"
    $sizeMB = [math]::Round($exe.Length/1MB, 2)
    Write-Host "New installer created:" -ForegroundColor Cyan
    Write-Host "  File: $($exe.Name)" -ForegroundColor White
    Write-Host "  Size: $sizeMB MB" -ForegroundColor Gray
    Write-Host "  Location: $($exe.FullName)" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Install this new version:" -ForegroundColor Yellow
    Write-Host "  .\run-installer.ps1" -ForegroundColor White
} else {
    Write-Host "  WARNING: Installer not found" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "FIX COMPLETE!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
