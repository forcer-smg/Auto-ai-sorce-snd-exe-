# ============================================================
# Install Dependencies and Rebuild
# ============================================================

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  INSTALLING DEPENDENCIES AND REBUILDING" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptPath

# Step 1: Add tools to toolkit
Write-Host "[1/5] Adding tools to RedTeam-Tools..." -ForegroundColor Yellow

$toolkitPath = Join-Path $scriptPath "RedTeam-Tools"
if (-not (Test-Path $toolkitPath)) {
    Write-Host "  Creating RedTeam-Tools directory..." -ForegroundColor Gray
    New-Item -ItemType Directory -Path $toolkitPath -Force | Out-Null
}

Set-Location $toolkitPath

# Add 365-Stealer
if (-not (Test-Path "365-Stealer")) {
    Write-Host "  Cloning 365-Stealer..." -ForegroundColor Gray
    git clone https://github.com/AlteredSecurity/365-Stealer.git 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  [+] 365-Stealer added" -ForegroundColor Green
    } else {
        Write-Host "  [!] Failed to clone 365-Stealer" -ForegroundColor Red
    }
} else {
    Write-Host "  [+] 365-Stealer already exists" -ForegroundColor Green
}

# Add requests-ip-rotator
if (-not (Test-Path "requests-ip-rotator")) {
    Write-Host "  Cloning requests-ip-rotator..." -ForegroundColor Gray
    git clone https://github.com/Ge0rg3/requests-ip-rotator.git 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  [+] requests-ip-rotator added" -ForegroundColor Green
    } else {
        Write-Host "  [!] Failed to clone requests-ip-rotator" -ForegroundColor Red
    }
} else {
    Write-Host "  [+] requests-ip-rotator already exists" -ForegroundColor Green
}

Set-Location $scriptPath

# Step 2: Install 365-Stealer dependencies
Write-Host ""
Write-Host "[2/5] Installing 365-Stealer dependencies..." -ForegroundColor Yellow
$stealerPath = Join-Path $toolkitPath "365-Stealer"
if (Test-Path $stealerPath) {
    Set-Location $stealerPath
    if (Test-Path "requirements.txt") {
        Write-Host "  Installing from requirements.txt..." -ForegroundColor Gray
        python -m pip install -q -r requirements.txt
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  [+] 365-Stealer dependencies installed" -ForegroundColor Green
        } else {
            Write-Host "  [!] Some dependencies may have failed" -ForegroundColor Yellow
        }
    } else {
        Write-Host "  [!] No requirements.txt found" -ForegroundColor Yellow
    }
    Set-Location $scriptPath
} else {
    Write-Host "  [!] 365-Stealer not found" -ForegroundColor Red
}

# Step 3: Install requests-ip-rotator dependencies
Write-Host ""
Write-Host "[3/5] Installing requests-ip-rotator dependencies..." -ForegroundColor Yellow
$rotatorPath = Join-Path $toolkitPath "requests-ip-rotator"
if (Test-Path $rotatorPath) {
    Set-Location $rotatorPath
    if (Test-Path "requirements.txt") {
        Write-Host "  Installing from requirements.txt..." -ForegroundColor Gray
        python -m pip install -q -r requirements.txt
    } else {
        Write-Host "  Installing requests-ip-rotator package..." -ForegroundColor Gray
        python -m pip install -q requests-ip-rotator
    }
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  [+] requests-ip-rotator dependencies installed" -ForegroundColor Green
    } else {
        Write-Host "  [!] Some dependencies may have failed" -ForegroundColor Yellow
    }
    Set-Location $scriptPath
} else {
    Write-Host "  [!] requests-ip-rotator not found" -ForegroundColor Red
}

# Step 4: Install main app dependencies
Write-Host ""
Write-Host "[4/5] Installing main app dependencies..." -ForegroundColor Yellow
if (Test-Path "requirements.txt") {
    Write-Host "  Installing from requirements.txt..." -ForegroundColor Gray
    python -m pip install -q -r requirements.txt
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  [+] Main app dependencies installed" -ForegroundColor Green
    } else {
        Write-Host "  [!] Some dependencies may have failed" -ForegroundColor Yellow
    }
} else {
    Write-Host "  [!] requirements.txt not found" -ForegroundColor Red
}

# Step 5: Rebuild app
Write-Host ""
Write-Host "[5/5] Rebuilding application..." -ForegroundColor Yellow
Write-Host ""

# Close any running processes first
Write-Host "  Closing running processes..." -ForegroundColor Gray
Get-Process | Where-Object {
    $_.ProcessName -like "*Auto_Punch*" -or 
    $_.ProcessName -like "*electron*"
} | Stop-Process -Force -ErrorAction SilentlyContinue

Get-Process python -ErrorAction SilentlyContinue | Where-Object {
    (Get-WmiObject Win32_Process -Filter "ProcessId = $($_.Id)").CommandLine -like "*app.py*"
} | Stop-Process -Force -ErrorAction SilentlyContinue

Start-Sleep -Seconds 2

# Rebuild
Write-Host "  Running build..." -ForegroundColor Gray
npm run build:exe

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "============================================================" -ForegroundColor Green
    Write-Host "  BUILD SUCCESSFUL!" -ForegroundColor Green
    Write-Host "============================================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Tools added:" -ForegroundColor Cyan
    Write-Host "  ✓ 365-Stealer" -ForegroundColor Green
    Write-Host "  ✓ requests-ip-rotator" -ForegroundColor Green
    Write-Host ""
    Write-Host "Dependencies installed and app rebuilt!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Test the build with:" -ForegroundColor Yellow
    Write-Host "  .\TEST_BUILD.ps1" -ForegroundColor Cyan
} else {
    Write-Host ""
    Write-Host "============================================================" -ForegroundColor Red
    Write-Host "  BUILD FAILED" -ForegroundColor Red
    Write-Host "============================================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "Check the error messages above." -ForegroundColor Yellow
}

Write-Host ""
Read-Host "Press Enter to exit"

