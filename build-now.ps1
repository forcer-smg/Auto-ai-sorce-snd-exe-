# Quick Build Script
# Run: .\build-now.ps1

# Refresh PATH
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

Set-Location -Path "C:\Users\Administrator\Auto_Punch IDE"

Write-Host ""
Write-Host "Building installers..." -ForegroundColor Yellow
Write-Host "This will take 20-30 minutes. Please wait..." -ForegroundColor Gray
Write-Host ""

& npm run build:all

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "BUILD COMPLETE!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Installers in dist\ folder:" -ForegroundColor Cyan
    Get-ChildItem "dist\*.msi", "dist\*.exe" -ErrorAction SilentlyContinue | ForEach-Object {
        Write-Host "  $($_.Name)" -ForegroundColor Green
    }
} else {
    Write-Host ""
    Write-Host "Build failed. Check errors above." -ForegroundColor Red
}


