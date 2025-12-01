# Verify and Fix All Issues
# Run: .\verify-and-fix.ps1

Set-Location -Path "C:\Users\Administrator\Auto_Punch IDE"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "VERIFY AND FIX ALL ISSUES" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$errors = @()
$warnings = @()

# Check 1: Node.js
Write-Host "[1/8] Checking Node.js..." -ForegroundColor Yellow
try {
    $nodeVersion = & node --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✓ Node.js: $nodeVersion" -ForegroundColor Green
    } else {
        $errors += "Node.js not found"
        Write-Host "  ✗ Node.js not found" -ForegroundColor Red
    }
} catch {
    $errors += "Node.js not installed"
    Write-Host "  ✗ Node.js not installed" -ForegroundColor Red
}

# Check 2: npm
Write-Host "[2/8] Checking npm..." -ForegroundColor Yellow
try {
    $npmVersion = & npm --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✓ npm: $npmVersion" -ForegroundColor Green
    } else {
        $errors += "npm not found"
        Write-Host "  ✗ npm not found" -ForegroundColor Red
    }
} catch {
    $errors += "npm not installed"
    Write-Host "  ✗ npm not installed" -ForegroundColor Red
}

# Check 3: Dependencies
Write-Host "[3/8] Checking dependencies..." -ForegroundColor Yellow
if (Test-Path "node_modules\electron") {
    Write-Host "  ✓ Electron installed" -ForegroundColor Green
} else {
    $errors += "Electron not installed"
    Write-Host "  ✗ Electron not installed" -ForegroundColor Red
    Write-Host "    Fixing: Running npm install..." -ForegroundColor Yellow
    & npm install 2>&1 | Out-Null
}

if (Test-Path "node_modules\electron-builder") {
    Write-Host "  ✓ electron-builder installed" -ForegroundColor Green
} else {
    $errors += "electron-builder not installed"
    Write-Host "  ✗ electron-builder not installed" -ForegroundColor Red
}

# Check 4: Configuration
Write-Host "[4/8] Checking configuration..." -ForegroundColor Yellow
if (Test-Path "package.json") {
    $pkg = Get-Content "package.json" | ConvertFrom-Json
    if ($pkg.build.win.icon) {
        $warnings += "Icon configured but file may not exist"
        Write-Host "  ⚠ Icon configured" -ForegroundColor Yellow
    } else {
        Write-Host "  ✓ No icon issues (using default)" -ForegroundColor Green
    }
    Write-Host "  ✓ package.json valid" -ForegroundColor Green
} else {
    $errors += "package.json not found"
    Write-Host "  ✗ package.json not found" -ForegroundColor Red
}

# Check 5: Electron files
Write-Host "[5/8] Checking Electron files..." -ForegroundColor Yellow
if (Test-Path "electron\main.js") {
    Write-Host "  ✓ main.js found" -ForegroundColor Green
} else {
    $errors += "electron/main.js not found"
    Write-Host "  ✗ main.js not found" -ForegroundColor Red
}

if (Test-Path "electron\preload.js") {
    Write-Host "  ✓ preload.js found" -ForegroundColor Green
} else {
    $warnings += "electron/preload.js not found (optional)"
    Write-Host "  ⚠ preload.js not found (optional)" -ForegroundColor Yellow
}

# Check 6: Build output
Write-Host "[6/8] Checking build output..." -ForegroundColor Yellow
$installerPath = "dist\Auto_Punch IDE Setup 1.0.0.exe"
if (Test-Path $installerPath) {
    $exe = Get-Item $installerPath
    Write-Host "  ✓ Installer found: $([math]::Round($exe.Length/1MB, 2)) MB" -ForegroundColor Green
} else {
    $warnings += "Installer not built yet"
    Write-Host "  ⚠ Installer not found" -ForegroundColor Yellow
    Write-Host "    Run: npm run build:exe" -ForegroundColor Gray
}

# Check 7: Python/Flask
Write-Host "[7/8] Checking Python processes..." -ForegroundColor Yellow
$pythonProcs = Get-Process | Where-Object {$_.ProcessName -eq "python" -or $_.ProcessName -eq "pythonw"}
if ($pythonProcs) {
    Write-Host "  ⚠ Python processes running (may interfere)" -ForegroundColor Yellow
    Write-Host "    Stopping..." -ForegroundColor Gray
    $pythonProcs | Stop-Process -Force -ErrorAction SilentlyContinue
    Write-Host "  ✓ Processes stopped" -ForegroundColor Green
} else {
    Write-Host "  ✓ No interfering processes" -ForegroundColor Green
}

# Check 8: File permissions
Write-Host "[8/8] Checking file permissions..." -ForegroundColor Yellow
try {
    $testFile = "test-write.tmp"
    "test" | Out-File $testFile -ErrorAction Stop
    Remove-Item $testFile -ErrorAction Stop
    Write-Host "  ✓ Write permissions OK" -ForegroundColor Green
} catch {
    $errors += "Write permissions issue"
    Write-Host "  ✗ Write permissions issue" -ForegroundColor Red
}

# Summary
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "VERIFICATION SUMMARY" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

if ($errors.Count -eq 0) {
    Write-Host "✅ No critical errors!" -ForegroundColor Green
} else {
    Write-Host "❌ Critical errors found:" -ForegroundColor Red
    $errors | ForEach-Object {
        Write-Host "  - $_" -ForegroundColor Red
    }
}

if ($warnings.Count -gt 0) {
    Write-Host ""
    Write-Host "⚠️  Warnings:" -ForegroundColor Yellow
    $warnings | ForEach-Object {
        Write-Host "  - $_" -ForegroundColor Yellow
    }
}

Write-Host ""
if ($errors.Count -eq 0) {
    Write-Host "✅ Everything is ready!" -ForegroundColor Green
    Write-Host "   Run: .\auto-run-all.ps1" -ForegroundColor Cyan
} else {
    Write-Host "❌ Please fix errors above" -ForegroundColor Red
}
Write-Host ""


