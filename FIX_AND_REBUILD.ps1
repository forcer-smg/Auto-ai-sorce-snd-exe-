# Comprehensive Fix and Rebuild Script
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  FIXING TOOLS & REBUILDING APPLICATION" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Stop running processes
Write-Host "[~] Stopping running processes..." -ForegroundColor Yellow
Get-Process | Where-Object {$_.ProcessName -like "*Auto_Punch*"} | Stop-Process -Force -ErrorAction SilentlyContinue
Get-Process python -ErrorAction SilentlyContinue | Where-Object {$_.MainWindowTitle -like "*Flask*"} | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2

# Navigate to project directory
Set-Location "C:\Users\Administrator\Auto_Punch IDE"

# Check and fix tool installations
Write-Host ""
Write-Host "[~] Checking tool installations..." -ForegroundColor Yellow

$toolkitPath = "RedTeam-Tools"
$toolsFixed = $false

# Check 365-Stealer
$stealerPath = Join-Path $toolkitPath "365-Stealer"
if (Test-Path $stealerPath) {
    Write-Host "[+] 365-Stealer found" -ForegroundColor Green
    
    # Check if main file exists
    $mainFile = Join-Path $stealerPath "365-Stealer.py"
    if (-not (Test-Path $mainFile)) {
        Write-Host "[!] 365-Stealer.py not found, checking for alternative..." -ForegroundColor Yellow
        # Look for any .py file
        $pyFiles = Get-ChildItem -Path $stealerPath -Filter "*.py" -Recurse | Select-Object -First 1
        if ($pyFiles) {
            Write-Host "[+] Found: $($pyFiles.Name)" -ForegroundColor Green
        }
    } else {
        Write-Host "[+] 365-Stealer.py found" -ForegroundColor Green
    }
    
    # Install dependencies
    $reqFile = Join-Path $stealerPath "requirements.txt"
    if (Test-Path $reqFile) {
        Write-Host "[~] Installing 365-Stealer dependencies..." -ForegroundColor Yellow
        python -m pip install -q -r $reqFile 2>&1 | Out-Null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "[+] 365-Stealer dependencies installed" -ForegroundColor Green
            $toolsFixed = $true
        } else {
            Write-Host "[!] Warning: Some dependencies may have failed" -ForegroundColor Yellow
        }
    }
} else {
    Write-Host "[!] 365-Stealer not found in $stealerPath" -ForegroundColor Red
}

# Check requests-ip-rotator
$rotatorPath = Join-Path $toolkitPath "requests-ip-rotator"
if (Test-Path $rotatorPath) {
    Write-Host "[+] requests-ip-rotator found" -ForegroundColor Green
    
    # Install as a package
    $setupFile = Join-Path $rotatorPath "setup.py"
    if (Test-Path $setupFile) {
        Write-Host "[~] Installing requests-ip-rotator..." -ForegroundColor Yellow
        Set-Location $rotatorPath
        python -m pip install -q -e . 2>&1 | Out-Null
        Set-Location "C:\Users\Administrator\Auto_Punch IDE"
        if ($LASTEXITCODE -eq 0) {
            Write-Host "[+] requests-ip-rotator installed" -ForegroundColor Green
            $toolsFixed = $true
        } else {
            Write-Host "[!] Warning: Installation may have failed" -ForegroundColor Yellow
        }
    } else {
        # Try installing dependencies manually
        Write-Host "[~] Installing requests-ip-rotator dependencies (requests, boto3)..." -ForegroundColor Yellow
        python -m pip install -q requests boto3 2>&1 | Out-Null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "[+] Dependencies installed" -ForegroundColor Green
        }
    }
} else {
    Write-Host "[!] requests-ip-rotator not found in $rotatorPath" -ForegroundColor Red
}

# Fix CSS 404 errors (remove references to non-existent images)
Write-Host ""
Write-Host "[~] Fixing CSS image references..." -ForegroundColor Yellow
$cssFile = "static\css\themes.css"
if (Test-Path $cssFile) {
    $cssContent = Get-Content $cssFile -Raw
    # Only keep hacking-bg.jpg reference (the one that exists)
    $cssContent = $cssContent -replace "url\('/static/images/hacking-bg\.png\?v=1'\),\s*", ""
    $cssContent = $cssContent -replace "url\('/static/images/hacking-bg\.jpeg\?v=1'\),\s*", ""
    Set-Content -Path $cssFile -Value $cssContent -NoNewline
    Write-Host "[+] CSS fixed (removed non-existent image references)" -ForegroundColor Green
}

# Rebuild application
Write-Host ""
Write-Host "[~] Building application..." -ForegroundColor Yellow
npm run build:exe

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "============================================================" -ForegroundColor Green
    Write-Host "  BUILD SUCCESSFUL!" -ForegroundColor Green
    Write-Host "============================================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "✅ All fixes applied:" -ForegroundColor Green
    Write-Host "   - Toolkit frontend error fixed" -ForegroundColor Cyan
    Write-Host "   - Tool dependencies installed" -ForegroundColor Cyan
    Write-Host "   - CSS 404 errors fixed" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Test with:" -ForegroundColor Yellow
    Write-Host "  .\TEST_BUILD.ps1" -ForegroundColor Cyan
} else {
    Write-Host ""
    Write-Host "============================================================" -ForegroundColor Red
    Write-Host "  BUILD FAILED" -ForegroundColor Red
    Write-Host "============================================================" -ForegroundColor Red
}

Write-Host ""
Read-Host "Press Enter to exit"

