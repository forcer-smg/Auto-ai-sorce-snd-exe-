# Build EXE Installer Only (NSIS - More Reliable)
# Run: .\build-exe-only.ps1

$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

Set-Location -Path "C:\Users\Administrator\Auto_Punch IDE"

Write-Host ""
Write-Host "Building EXE installer (NSIS)..." -ForegroundColor Yellow
Write-Host "This will take 10-15 minutes. Please wait..." -ForegroundColor Gray
Write-Host ""

& npm run build:exe

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "BUILD COMPLETE!" -ForegroundColor Green
    Write-Host ""
    Write-Host "EXE installer created in dist\ folder:" -ForegroundColor Cyan
    Get-ChildItem "dist\*.exe" -ErrorAction SilentlyContinue | ForEach-Object {
        Write-Host "  $($_.Name)" -ForegroundColor Green
    }
    Write-Host ""
    Write-Host "You can distribute this EXE installer!" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "Build failed. Check errors above." -ForegroundColor Red
}


