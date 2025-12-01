# Direct Build - No Fancy Scripts
# Run: .\build-direct.ps1

cd "C:\Users\Administrator\Auto_Punch IDE"

Write-Host "Building installer..." -ForegroundColor Yellow
Write-Host ""

$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

npm run build:exe

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "Build complete!" -ForegroundColor Green
    if (Test-Path "dist\Auto_Punch IDE Setup 1.0.0.exe") {
        Write-Host "Installer: dist\Auto_Punch IDE Setup 1.0.0.exe" -ForegroundColor Cyan
    }
} else {
    Write-Host ""
    Write-Host "Build failed!" -ForegroundColor Red
}


