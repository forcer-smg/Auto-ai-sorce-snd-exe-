# ============================================================
# Add Tools to RedTeam-Tools Toolkit
# ============================================================

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  ADDING TOOLS TO REDTEAM-TOOLS" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$toolkitPath = Join-Path $scriptPath "RedTeam-Tools"

# Check if RedTeam-Tools exists
if (-not (Test-Path $toolkitPath)) {
    Write-Host "[!] RedTeam-Tools directory not found!" -ForegroundColor Red
    Write-Host "    Creating directory..." -ForegroundColor Yellow
    New-Item -ItemType Directory -Path $toolkitPath -Force | Out-Null
}

Set-Location $toolkitPath

# Tool 1: 365-Stealer
Write-Host ""
Write-Host "[1/2] Adding 365-Stealer..." -ForegroundColor Yellow
if (Test-Path "365-Stealer") {
    Write-Host "  [!] 365-Stealer already exists, updating..." -ForegroundColor Gray
    Set-Location "365-Stealer"
    git pull 2>&1 | Out-Null
    Set-Location ..
} else {
    Write-Host "  [~] Cloning 365-Stealer..." -ForegroundColor Gray
    git clone https://github.com/AlteredSecurity/365-Stealer.git 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  [+] 365-Stealer added successfully" -ForegroundColor Green
    } else {
        Write-Host "  [!] Failed to clone 365-Stealer" -ForegroundColor Red
    }
}

# Tool 2: requests-ip-rotator
Write-Host ""
Write-Host "[2/2] Adding requests-ip-rotator..." -ForegroundColor Yellow
if (Test-Path "requests-ip-rotator") {
    Write-Host "  [!] requests-ip-rotator already exists, updating..." -ForegroundColor Gray
    Set-Location "requests-ip-rotator"
    git pull 2>&1 | Out-Null
    Set-Location ..
} else {
    Write-Host "  [~] Cloning requests-ip-rotator..." -ForegroundColor Gray
    git clone https://github.com/Ge0rg3/requests-ip-rotator.git 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  [+] requests-ip-rotator added successfully" -ForegroundColor Green
    } else {
        Write-Host "  [!] Failed to clone requests-ip-rotator" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host "  TOOLS ADDED TO TOOLKIT" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Tools added:" -ForegroundColor Cyan
Write-Host "  ✓ 365-Stealer - Phishing simulation tool" -ForegroundColor Green
Write-Host "  ✓ requests-ip-rotator - IP rotation for requests" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Install dependencies for each tool" -ForegroundColor Gray
Write-Host "  2. Configure tools as needed" -ForegroundColor Gray
Write-Host "  3. Rebuild the app to include new tools" -ForegroundColor Gray
Write-Host ""
Read-Host "Press Enter to exit"

