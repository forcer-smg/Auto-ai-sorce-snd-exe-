# Final Build - Production Software Application
# Run: .\final-build.ps1

Set-Location -Path "C:\Users\Administrator\Auto_Punch IDE"

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "FINAL BUILD - PRODUCTION SOFTWARE" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

# Step 1: Verify everything
Write-Host "[1/5] Verifying setup..." -ForegroundColor Yellow
$machinePath = [System.Environment]::GetEnvironmentVariable("Path","Machine")
$userPath = [System.Environment]::GetEnvironmentVariable("Path","User")
$env:Path = $machinePath + ";" + $userPath

try {
    $nodeVersion = & node --version 2>&1
    $npmVersion = & npm --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  Node.js: $nodeVersion" -ForegroundColor Green
        Write-Host "  npm: $npmVersion" -ForegroundColor Green
    } else {
        throw "Node.js not found"
    }
} catch {
    Write-Host "  ERROR: Node.js not found!" -ForegroundColor Red
    exit 1
}

if (Test-Path "node_modules\electron") {
    Write-Host "  Electron: Ready" -ForegroundColor Green
} else {
    Write-Host "  Installing dependencies..." -ForegroundColor Yellow
    & npm install
}
Write-Host ""

# Step 2: Clean old builds
Write-Host "[2/5] Cleaning old builds..." -ForegroundColor Yellow
Remove-Item -Path "dist" -Recurse -Force -ErrorAction SilentlyContinue
Write-Host "  Cleaned" -ForegroundColor Green
Write-Host ""

# Step 3: Build installer
Write-Host "[3/5] Building production installer..." -ForegroundColor Yellow
Write-Host "  This will take 10-15 minutes..." -ForegroundColor Gray
Write-Host ""

& npm run build:exe

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "  ERROR: Build failed!" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Step 4: Verify build
Write-Host "[4/5] Verifying build..." -ForegroundColor Yellow
$installerPath = "dist\Auto_Punch IDE Setup 1.0.0.exe"

if (Test-Path $installerPath) {
    $exe = Get-Item $installerPath
    $sizeMB = [math]::Round($exe.Length/1MB, 2)
    Write-Host "  Installer created: $sizeMB MB" -ForegroundColor Green
    Write-Host "  Location: $($exe.FullName)" -ForegroundColor Gray
} else {
    Write-Host "  ERROR: Installer not found!" -ForegroundColor Red
    exit 1
}

if (Test-Path "dist\win-unpacked\Auto_Punch IDE.exe") {
    Write-Host "  Portable app ready" -ForegroundColor Green
}
Write-Host ""

# Step 5: Create distribution package
Write-Host "[5/5] Creating distribution package..." -ForegroundColor Yellow

$distFolder = "dist\distribution"
New-Item -ItemType Directory -Path $distFolder -Force | Out-Null

# Copy installer
Copy-Item $installerPath -Destination $distFolder -Force

# Create README
$readme = @"
# Auto_Punch IDE - Installation

## Installer
- Auto_Punch IDE Setup 1.0.0.exe

## System Requirements
- Windows 10/11 (64-bit)
- Python 3.11+ (must be installed separately)
- 500 MB free disk space
- Internet connection (for initial setup)

## Installation
1. Double-click: Auto_Punch IDE Setup 1.0.0.exe
2. Follow the installation wizard
3. Launch from Start Menu or Desktop shortcut

## Important Notes
- Python must be installed before running the app
- Install Python from: https://www.python.org/downloads/
- The app will check for Python on first launch

## Portable Version
If you prefer a portable version:
- Location: dist\win-unpacked\Auto_Punch IDE.exe
- No installation needed
- Run directly from folder

## Support
For issues or questions, check the documentation files.
"@

$readme | Out-File "$distFolder\README.txt" -Encoding UTF8

Write-Host "  Distribution package created" -ForegroundColor Green
Write-Host ""

# Summary
Write-Host "========================================" -ForegroundColor Green
Write-Host "BUILD COMPLETE!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

Write-Host "Your software application is ready!" -ForegroundColor Cyan
Write-Host ""

Write-Host "Installer:" -ForegroundColor Yellow
Write-Host "  $($exe.FullName)" -ForegroundColor White
Write-Host "  Size: $sizeMB MB" -ForegroundColor Gray
Write-Host ""

Write-Host "Distribution Package:" -ForegroundColor Yellow
Write-Host "  $distFolder" -ForegroundColor White
Write-Host ""

Write-Host "Next Steps:" -ForegroundColor Cyan
Write-Host "  1. Test installer: .\run-installer.ps1" -ForegroundColor White
Write-Host "  2. Distribute the installer file" -ForegroundColor White
Write-Host "  3. Share with users" -ForegroundColor White
Write-Host ""

Write-Host "Opening distribution folder..." -ForegroundColor Yellow
Start-Sleep -Seconds 1
explorer $distFolder

Write-Host ""


