# Complete System Check for Build
# Run: .\check-system.ps1

Set-Location -Path "C:\Users\Administrator\Auto_Punch IDE"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "COMPLETE SYSTEM CHECK" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$allGood = $true
$warnings = @()
$errors = @()

# Check 1: Node.js
Write-Host "[1/10] Checking Node.js..." -ForegroundColor Yellow
$machinePath = [System.Environment]::GetEnvironmentVariable("Path","Machine")
$userPath = [System.Environment]::GetEnvironmentVariable("Path","User")
$env:Path = $machinePath + ";" + $userPath

$nodeFound = $false
$nodeVersion = ""
$nodePath = ""

try {
    $nodeVersion = & node --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        $nodePath = (Get-Command node).Source
        $nodeFound = $true
        Write-Host "  Node.js: $nodeVersion" -ForegroundColor Green
        Write-Host "  Path: $nodePath" -ForegroundColor Gray
    } else {
        throw "Not in PATH"
    }
} catch {
    # Try common locations
    $commonPaths = @(
        "C:\Program Files\nodejs\node.exe",
        "C:\Program Files (x86)\nodejs\node.exe",
        "$env:LOCALAPPDATA\Programs\nodejs\node.exe"
    )
    
    foreach ($path in $commonPaths) {
        if (Test-Path $path) {
            $nodePath = $path
            $nodeVersion = & $path --version 2>&1
            $nodeFound = $true
            Write-Host "  Node.js: $nodeVersion" -ForegroundColor Green
            Write-Host "  Path: $nodePath" -ForegroundColor Gray
            break
        }
    }
    
    if (-not $nodeFound) {
        $errors += "Node.js not found"
        Write-Host "  ERROR: Node.js not found!" -ForegroundColor Red
        Write-Host "    Install from: https://nodejs.org/" -ForegroundColor Yellow
        $allGood = $false
    }
}
Write-Host ""

# Check 2: npm
Write-Host "[2/10] Checking npm..." -ForegroundColor Yellow
if ($nodeFound) {
    try {
        if ($nodePath -eq "node") {
            $npmVersion = & npm --version 2>&1
        } else {
            $npmPath = Join-Path (Split-Path $nodePath) "npm.cmd"
            $npmVersion = & $npmPath --version 2>&1
        }
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  npm: $npmVersion" -ForegroundColor Green
        } else {
            throw "npm not working"
        }
    } catch {
        $errors += "npm not working"
        Write-Host "  ERROR: npm not working!" -ForegroundColor Red
        $allGood = $false
    }
} else {
    Write-Host "  SKIPPED: Node.js not found" -ForegroundColor Gray
}
Write-Host ""

# Check 3: Python
Write-Host "[3/10] Checking Python..." -ForegroundColor Yellow
$pythonFound = $false
$pythonVersion = ""
$pythonPath = ""

try {
    $pythonVersion = & python --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        $pythonPath = (Get-Command python).Source
        $pythonFound = $true
        Write-Host "  Python: $pythonVersion" -ForegroundColor Green
        Write-Host "  Path: $pythonPath" -ForegroundColor Gray
        
        # Check version number
        if ($pythonVersion -match "3\.(\d+)") {
            $minorVersion = [int]$matches[1]
            if ($minorVersion -lt 11) {
                $warnings += "Python version should be 3.11+ (found $pythonVersion)"
                Write-Host "  WARNING: Python 3.11+ recommended" -ForegroundColor Yellow
            }
        }
    } else {
        throw "Not in PATH"
    }
} catch {
    $commonPaths = @(
        "C:\Python314\python.exe",
        "C:\Python313\python.exe",
        "C:\Python312\python.exe",
        "C:\Python311\python.exe",
        "C:\Program Files\Python314\python.exe",
        "C:\Program Files\Python313\python.exe"
    )
    
    foreach ($path in $commonPaths) {
        if (Test-Path $path) {
            $pythonPath = $path
            $pythonVersion = & $path --version 2>&1
            $pythonFound = $true
            Write-Host "  Python: $pythonVersion" -ForegroundColor Green
            Write-Host "  Path: $pythonPath" -ForegroundColor Gray
            break
        }
    }
    
    if (-not $pythonFound) {
        $warnings += "Python not found (needed for Flask backend)"
        Write-Host "  WARNING: Python not found" -ForegroundColor Yellow
        Write-Host "    Install from: https://www.python.org/downloads/" -ForegroundColor Gray
    }
}
Write-Host ""

# Check 4: Disk Space
Write-Host "[4/10] Checking disk space..." -ForegroundColor Yellow
$drive = Get-PSDrive C
$freeGB = [math]::Round($drive.Free/1GB, 2)
$usedGB = [math]::Round($drive.Used/1GB, 2)
$totalGB = [math]::Round(($drive.Free + $drive.Used)/1GB, 2)

Write-Host "  Free: $freeGB GB" -ForegroundColor $(if ($freeGB -lt 2) { "Red" } elseif ($freeGB -lt 5) { "Yellow" } else { "Green" })
Write-Host "  Used: $usedGB GB" -ForegroundColor Gray
Write-Host "  Total: $totalGB GB" -ForegroundColor Gray

if ($freeGB -lt 0.5) {
    $errors += "Less than 500 MB free space"
    Write-Host "  ERROR: Insufficient disk space!" -ForegroundColor Red
    $allGood = $false
} elseif ($freeGB -lt 2) {
    $warnings += "Less than 2 GB free (build may fail)"
    Write-Host "  WARNING: Low disk space" -ForegroundColor Yellow
}
Write-Host ""

# Check 5: Required Files
Write-Host "[5/10] Checking required files..." -ForegroundColor Yellow
$requiredFiles = @(
    "package.json",
    "electron\main.js",
    "app.py",
    "requirements.txt"
)

foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Host "  $file - OK" -ForegroundColor Green
    } else {
        $errors += "$file missing"
        Write-Host "  $file - MISSING" -ForegroundColor Red
        $allGood = $false
    }
}
Write-Host ""

# Check 6: Node Dependencies
Write-Host "[6/10] Checking Node.js dependencies..." -ForegroundColor Yellow
if ($nodeFound) {
    if (Test-Path "node_modules\electron") {
        Write-Host "  Electron: Installed" -ForegroundColor Green
    } else {
        $warnings += "Electron not installed"
        Write-Host "  WARNING: Electron not installed" -ForegroundColor Yellow
        Write-Host "    Run: npm install" -ForegroundColor Gray
    }
    
    if (Test-Path "node_modules\electron-builder") {
        Write-Host "  electron-builder: Installed" -ForegroundColor Green
    } else {
        $warnings += "electron-builder not installed"
        Write-Host "  WARNING: electron-builder not installed" -ForegroundColor Yellow
        Write-Host "    Run: npm install" -ForegroundColor Gray
    }
} else {
    Write-Host "  SKIPPED: Node.js not found" -ForegroundColor Gray
}
Write-Host ""

# Check 7: Python Dependencies
Write-Host "[7/10] Checking Python dependencies..." -ForegroundColor Yellow
if ($pythonFound) {
    try {
        $flaskCheck = & python -c "import flask; print(flask.__version__)" 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  Flask: $flaskCheck" -ForegroundColor Green
        } else {
            $warnings += "Flask not installed"
            Write-Host "  WARNING: Flask not installed" -ForegroundColor Yellow
            Write-Host "    Run: pip install -r requirements.txt" -ForegroundColor Gray
        }
    } catch {
        $warnings += "Could not check Flask"
        Write-Host "  WARNING: Could not verify Flask" -ForegroundColor Yellow
    }
} else {
    Write-Host "  SKIPPED: Python not found" -ForegroundColor Gray
}
Write-Host ""

# Check 8: Port Availability
Write-Host "[8/10] Checking port 5001..." -ForegroundColor Yellow
$portInUse = Get-NetTCPConnection -LocalPort 5001 -ErrorAction SilentlyContinue
if ($portInUse) {
    $warnings += "Port 5001 is in use"
    Write-Host "  WARNING: Port 5001 is in use" -ForegroundColor Yellow
    Write-Host "    Process: $($portInUse.OwningProcess)" -ForegroundColor Gray
    Write-Host "    This is OK if Flask is already running" -ForegroundColor Gray
} else {
    Write-Host "  Port 5001 is available" -ForegroundColor Green
}
Write-Host ""

# Check 9: Internet Connection
Write-Host "[9/10] Checking internet connection..." -ForegroundColor Yellow
try {
    $ping = Test-Connection -ComputerName "8.8.8.8" -Count 1 -Quiet -ErrorAction Stop
    if ($ping) {
        Write-Host "  Internet: Connected" -ForegroundColor Green
    } else {
        $warnings += "Internet connection may be slow"
        Write-Host "  WARNING: Internet connection may be slow" -ForegroundColor Yellow
    }
} catch {
    $warnings += "Could not verify internet connection"
    Write-Host "  WARNING: Could not verify internet" -ForegroundColor Yellow
    Write-Host "    Build may fail if downloads are needed" -ForegroundColor Gray
}
Write-Host ""

# Check 10: Build Tools
Write-Host "[10/10] Checking build tools..." -ForegroundColor Yellow
if ($nodeFound) {
    if (Test-Path "node_modules\.bin\electron-builder.cmd") {
        Write-Host "  electron-builder: Ready" -ForegroundColor Green
    } else {
        $warnings += "electron-builder binary not found"
        Write-Host "  WARNING: electron-builder binary not found" -ForegroundColor Yellow
    }
} else {
    Write-Host "  SKIPPED: Node.js not found" -ForegroundColor Gray
}
Write-Host ""

# Summary
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "SYSTEM CHECK SUMMARY" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

if ($errors.Count -eq 0 -and $warnings.Count -eq 0) {
    Write-Host "ALL CHECKS PASSED!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Your system is ready to build!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next step:" -ForegroundColor Cyan
    Write-Host "  .\BUILD_ROBUST.bat" -ForegroundColor White
} else {
    if ($errors.Count -gt 0) {
        Write-Host "CRITICAL ERRORS:" -ForegroundColor Red
        $errors | ForEach-Object {
            Write-Host "  - $_" -ForegroundColor Red
        }
        Write-Host ""
        Write-Host "Please fix these errors before building." -ForegroundColor Red
        $allGood = $false
    }
    
    if ($warnings.Count -gt 0) {
        Write-Host "WARNINGS:" -ForegroundColor Yellow
        $warnings | ForEach-Object {
            Write-Host "  - $_" -ForegroundColor Yellow
        }
        Write-Host ""
        Write-Host "These may cause issues but won't prevent building." -ForegroundColor Yellow
    }
    
    if ($allGood) {
        Write-Host ""
        Write-Host "System is ready (with warnings)" -ForegroundColor Green
        Write-Host "You can proceed with building." -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""


