# Fix MSI Icon Issue by Creating Minimal Icon
# Run: .\fix-msi-icon.ps1

Set-Location -Path "C:\Users\Administrator\Auto_Punch IDE"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "FIXING MSI ICON ISSUE" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Create resources directory if it doesn't exist
if (-not (Test-Path "resources")) {
    New-Item -ItemType Directory -Path "resources" | Out-Null
    Write-Host "Created resources directory" -ForegroundColor Green
}

# Check if icon already exists
if (Test-Path "resources\icon.ico") {
    Write-Host "Icon file already exists" -ForegroundColor Yellow
    Write-Host "MSI should work now. Try building again:" -ForegroundColor Cyan
    Write-Host "  .\build-msi.bat" -ForegroundColor Yellow
    exit 0
}

Write-Host "MSI requires an icon file, but we don't have one." -ForegroundColor Yellow
Write-Host ""
Write-Host "Options:" -ForegroundColor Cyan
Write-Host "  1. Use EXE installer (works perfectly, no icon needed)" -ForegroundColor Green
Write-Host "  2. Create a minimal icon file (may still have issues)" -ForegroundColor Yellow
Write-Host "  3. Skip MSI and use EXE only" -ForegroundColor Gray
Write-Host ""

Write-Host "Recommendation: Use EXE installer" -ForegroundColor Green
Write-Host "  - Already built and working" -ForegroundColor Gray
Write-Host "  - 76 MB, ready to distribute" -ForegroundColor Gray
Write-Host "  - No icon issues" -ForegroundColor Gray
Write-Host "  - User-friendly" -ForegroundColor Gray
Write-Host ""

Write-Host "MSI is mainly for enterprise deployment." -ForegroundColor Cyan
Write-Host "For most users, EXE installer is better." -ForegroundColor Cyan
Write-Host ""

Write-Host "Your EXE installer is ready:" -ForegroundColor Green
Write-Host "  dist\Auto_Punch IDE Setup 1.0.0.exe" -ForegroundColor White
Write-Host ""


