# Build MSI Installer
# Run: .\build-msi.ps1

Set-Location -Path "C:\Users\Administrator\Auto_Punch IDE"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "BUILDING MSI INSTALLER" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check disk space
Write-Host "[1/4] Checking disk space..." -ForegroundColor Yellow
$drive = Get-PSDrive C
$freeGB = [math]::Round($drive.Free/1GB, 2)
$usedGB = [math]::Round($drive.Used/1GB, 2)

Write-Host "  Free space: $freeGB GB" -ForegroundColor Cyan
Write-Host "  Used space: $usedGB GB" -ForegroundColor Gray

if ($freeGB -lt 2) {
    Write-Host "  WARNING: Low disk space! MSI build may fail." -ForegroundColor Yellow
    Write-Host "  Recommended: At least 2 GB free" -ForegroundColor Yellow
} else {
    Write-Host "  Disk space: OK" -ForegroundColor Green
}
Write-Host ""

# Refresh PATH
Write-Host "[2/4] Verifying Node.js..." -ForegroundColor Yellow
$machinePath = [System.Environment]::GetEnvironmentVariable("Path","Machine")
$userPath = [System.Environment]::GetEnvironmentVariable("Path","User")
$env:Path = $machinePath + ";" + $userPath

try {
    $nodeVersion = & node --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  Node.js: $nodeVersion" -ForegroundColor Green
    } else {
        throw "Node.js not found"
    }
} catch {
    Write-Host "  ERROR: Node.js not found!" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Clean old MSI build files
Write-Host "[3/4] Cleaning old MSI build files..." -ForegroundColor Yellow
Remove-Item -Path "dist\__msi-*" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "dist\*.msi" -Force -ErrorAction SilentlyContinue
Write-Host "  Cleaned" -ForegroundColor Green
Write-Host ""

# Build MSI
Write-Host "[4/4] Building MSI installer..." -ForegroundColor Yellow
Write-Host "  This will take 10-15 minutes..." -ForegroundColor Gray
Write-Host "  MSI installers are larger but better for enterprise deployment" -ForegroundColor Gray
Write-Host ""

& npm run build:msi

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "  ERROR: MSI build failed!" -ForegroundColor Red
    Write-Host ""
    Write-Host "  Common issues:" -ForegroundColor Yellow
    Write-Host "    1. Icon file missing (we removed icon references)" -ForegroundColor Gray
    Write-Host "    2. WiX toolset issues" -ForegroundColor Gray
    Write-Host "    3. Insufficient disk space" -ForegroundColor Gray
    Write-Host ""
    Write-Host "  Try EXE installer instead:" -ForegroundColor Cyan
    Write-Host "    npm run build:exe" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "MSI BUILD COMPLETE!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

if (Test-Path "dist\*.msi") {
    $msi = Get-Item "dist\*.msi" | Select-Object -First 1
    $sizeMB = [math]::Round($msi.Length/1MB, 2)
    Write-Host "MSI Installer:" -ForegroundColor Cyan
    Write-Host "  File: $($msi.Name)" -ForegroundColor White
    Write-Host "  Size: $sizeMB MB" -ForegroundColor Gray
    Write-Host "  Location: $($msi.FullName)" -ForegroundColor Gray
} else {
    Write-Host "  WARNING: MSI file not found in dist folder" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Opening dist folder..." -ForegroundColor Yellow
Start-Sleep -Seconds 1
explorer dist

Write-Host ""


