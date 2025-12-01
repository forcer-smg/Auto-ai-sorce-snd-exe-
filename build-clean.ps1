# Clean Build Script - Stops interfering processes first
# Run: .\build-clean.ps1

# Refresh PATH
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

Set-Location -Path "C:\Users\Administrator\Auto_Punch IDE"

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "Clean Build - Stopping Interfering Processes" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

# Stop Python/Flask processes
Write-Host "[1/3] Stopping background processes..." -ForegroundColor Yellow
Get-Process | Where-Object {$_.ProcessName -eq "python" -or $_.ProcessName -eq "pythonw"} | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2
Write-Host "  Done." -ForegroundColor Green
Write-Host ""

# Clean dist folder (optional)
Write-Host "[2/3] Cleaning old build files..." -ForegroundColor Yellow
Remove-Item -Path "dist\__*" -Recurse -Force -ErrorAction SilentlyContinue
Write-Host "  Done." -ForegroundColor Green
Write-Host ""

# Build
Write-Host "[3/3] Building EXE installer..." -ForegroundColor Yellow
Write-Host "  This will take 10-15 minutes. Please wait..." -ForegroundColor Gray
Write-Host ""

& npm run build:exe

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "BUILD COMPLETE!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "EXE installer created:" -ForegroundColor Cyan
    Get-ChildItem "dist\*.exe" -ErrorAction SilentlyContinue | ForEach-Object {
        Write-Host "  $($_.Name)" -ForegroundColor Green
    }
} else {
    Write-Host ""
    Write-Host "Build failed. Check errors above." -ForegroundColor Red
}


