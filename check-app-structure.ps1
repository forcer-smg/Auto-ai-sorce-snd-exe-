# Check App Structure - Without Cancellation Issues
# Run: .\check-app-structure.ps1

Set-Location -Path "C:\Users\Administrator\Auto_Punch IDE"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "APP STRUCTURE CHECK" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Checking key files and folders..." -ForegroundColor Yellow
Write-Host ""

# Core Files
$coreFiles = @(
    "app.py",
    "package.json",
    "electron\main.js",
    "templates\index.html",
    "requirements.txt"
)

Write-Host "Core Files:" -ForegroundColor Cyan
foreach ($file in $coreFiles) {
    if (Test-Path $file) {
        $item = Get-Item $file
        $size = if ($item.PSIsContainer) { "DIR" } else { "$([math]::Round($item.Length/1KB, 2)) KB" }
        Write-Host "  ✓ $file ($size)" -ForegroundColor Green
    } else {
        Write-Host "  ✗ $file (MISSING)" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "Folders:" -ForegroundColor Cyan
$folders = @("static", "templates", "electron", "dist", "node_modules")
foreach ($folder in $folders) {
    if (Test-Path $folder) {
        $item = Get-Item $folder
        if ($item.PSIsContainer) {
            $fileCount = (Get-ChildItem $folder -Recurse -File -ErrorAction SilentlyContinue).Count
            Write-Host "  ✓ $folder\ ($fileCount files)" -ForegroundColor Green
        }
    } else {
        Write-Host "  ✗ $folder\ (MISSING)" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "Build Output:" -ForegroundColor Cyan
if (Test-Path "dist\Auto_Punch IDE Setup 1.0.0.exe") {
    $exe = Get-Item "dist\Auto_Punch IDE Setup 1.0.0.exe"
    Write-Host "  ✓ Installer: $([math]::Round($exe.Length/1MB, 2)) MB" -ForegroundColor Green
} else {
    Write-Host "  ✗ Installer: NOT FOUND" -ForegroundColor Red
}

if (Test-Path "dist\win-unpacked") {
    $unpackedSize = ((Get-ChildItem "dist\win-unpacked" -Recurse -File -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum)
    Write-Host "  ✓ Portable: $([math]::Round($unpackedSize/1MB, 2)) MB" -ForegroundColor Green
} else {
    Write-Host "  ⚠ Portable: NOT FOUND" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""


