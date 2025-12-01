# Verify Build - Check if App is Well Built
# Run: .\verify-build.ps1

Set-Location -Path "C:\Users\Administrator\Auto_Punch IDE"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "VERIFYING BUILD" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$allGood = $true
$issues = @()

# Check 1: Installer File
Write-Host "[1/8] Checking installer..." -ForegroundColor Yellow
$installerPath = "dist\Auto_Punch IDE Setup 1.0.0.exe"
if (Test-Path $installerPath) {
    $exe = Get-Item $installerPath
    $sizeMB = [math]::Round($exe.Length/1MB, 2)
    Write-Host "  ✓ Installer found: $sizeMB MB" -ForegroundColor Green
    Write-Host "    Location: $($exe.FullName)" -ForegroundColor Gray
    Write-Host "    Created: $($exe.LastWriteTime)" -ForegroundColor Gray
    
    if ($sizeMB -lt 10) {
        $issues += "Installer seems too small (may be incomplete)"
        Write-Host "  ⚠ WARNING: Installer size seems small" -ForegroundColor Yellow
    } elseif ($sizeMB -gt 200) {
        Write-Host "  ⚠ NOTE: Installer is large (normal for Electron apps)" -ForegroundColor Yellow
    }
} else {
    $allGood = $false
    $issues += "Installer not found"
    Write-Host "  ✗ Installer not found!" -ForegroundColor Red
}
Write-Host ""

# Check 2: Portable App
Write-Host "[2/8] Checking portable app..." -ForegroundColor Yellow
$portablePath = "dist\win-unpacked\Auto_Punch IDE.exe"
if (Test-Path $portablePath) {
    $portable = Get-Item $portablePath
    $sizeMB = [math]::Round($portable.Length/1MB, 2)
    Write-Host "  ✓ Portable app found: $sizeMB MB" -ForegroundColor Green
} else {
    Write-Host "  ⚠ Portable app not found (optional)" -ForegroundColor Yellow
}
Write-Host ""

# Check 3: Electron Files
Write-Host "[3/8] Checking Electron files..." -ForegroundColor Yellow
if (Test-Path "electron\main.js") {
    $mainJs = Get-Item "electron\main.js"
    Write-Host "  ✓ main.js found ($([math]::Round($mainJs.Length/1KB, 2)) KB)" -ForegroundColor Green
} else {
    $allGood = $false
    $issues += "electron/main.js missing"
    Write-Host "  ✗ main.js not found!" -ForegroundColor Red
}

if (Test-Path "electron\preload.js") {
    Write-Host "  ✓ preload.js found" -ForegroundColor Green
} else {
    Write-Host "  ⚠ preload.js not found (optional)" -ForegroundColor Yellow
}
Write-Host ""

# Check 4: Python App Files
Write-Host "[4/8] Checking Python app files..." -ForegroundColor Yellow
if (Test-Path "app.py") {
    Write-Host "  ✓ app.py found" -ForegroundColor Green
} else {
    $allGood = $false
    $issues += "app.py missing"
    Write-Host "  ✗ app.py not found!" -ForegroundColor Red
}

if (Test-Path "requirements.txt") {
    Write-Host "  ✓ requirements.txt found" -ForegroundColor Green
} else {
    Write-Host "  ⚠ requirements.txt not found" -ForegroundColor Yellow
}
Write-Host ""

# Check 5: Templates and Static Files
Write-Host "[5/8] Checking web files..." -ForegroundColor Yellow
if (Test-Path "templates\index.html") {
    Write-Host "  ✓ templates/index.html found" -ForegroundColor Green
} else {
    Write-Host "  ⚠ templates/index.html not found" -ForegroundColor Yellow
}

if (Test-Path "static") {
    $staticFiles = (Get-ChildItem "static" -Recurse -File).Count
    Write-Host "  ✓ static folder found ($staticFiles files)" -ForegroundColor Green
} else {
    Write-Host "  ⚠ static folder not found" -ForegroundColor Yellow
}
Write-Host ""

# Check 6: Dependencies
Write-Host "[6/8] Checking dependencies..." -ForegroundColor Yellow
if (Test-Path "node_modules\electron") {
    Write-Host "  ✓ Electron installed" -ForegroundColor Green
} else {
    $allGood = $false
    $issues += "Electron not installed"
    Write-Host "  ✗ Electron not installed!" -ForegroundColor Red
}

if (Test-Path "node_modules\electron-builder") {
    Write-Host "  ✓ electron-builder installed" -ForegroundColor Green
} else {
    Write-Host "  ⚠ electron-builder not found" -ForegroundColor Yellow
}
Write-Host ""

# Check 7: Configuration
Write-Host "[7/8] Checking configuration..." -ForegroundColor Yellow
if (Test-Path "package.json") {
    $pkg = Get-Content "package.json" | ConvertFrom-Json
    Write-Host "  ✓ package.json found" -ForegroundColor Green
    Write-Host "    App ID: $($pkg.build.appId)" -ForegroundColor Gray
    Write-Host "    Product: $($pkg.build.productName)" -ForegroundColor Gray
    Write-Host "    Version: $($pkg.version)" -ForegroundColor Gray
} else {
    $allGood = $false
    $issues += "package.json missing"
    Write-Host "  ✗ package.json not found!" -ForegroundColor Red
}
Write-Host ""

# Check 8: Build Artifacts
Write-Host "[8/8] Checking build artifacts..." -ForegroundColor Yellow
if (Test-Path "dist") {
    $distFiles = Get-ChildItem "dist" -Recurse -File
    $distSize = ($distFiles | Measure-Object -Property Length -Sum).Sum
    $distSizeMB = [math]::Round($distSize/1MB, 2)
    Write-Host "  ✓ dist folder found ($distSizeMB MB total)" -ForegroundColor Green
    Write-Host "    Files: $($distFiles.Count)" -ForegroundColor Gray
} else {
    Write-Host "  ⚠ dist folder not found" -ForegroundColor Yellow
}
Write-Host ""

# Summary
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "VERIFICATION SUMMARY" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

if ($allGood -and $issues.Count -eq 0) {
    Write-Host "✅ BUILD VERIFICATION: PASSED" -ForegroundColor Green
    Write-Host ""
    Write-Host "Your app is well built and ready!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Installer ready:" -ForegroundColor Cyan
    Write-Host "  $installerPath" -ForegroundColor White
} else {
    Write-Host "⚠️  BUILD VERIFICATION: ISSUES FOUND" -ForegroundColor Yellow
    Write-Host ""
    if ($issues.Count -gt 0) {
        Write-Host "Issues:" -ForegroundColor Red
        $issues | ForEach-Object {
            Write-Host "  - $_" -ForegroundColor Red
        }
        Write-Host ""
    }
    if ($allGood) {
        Write-Host "Minor issues only - app should still work" -ForegroundColor Yellow
    } else {
        Write-Host "Critical issues found - may need to rebuild" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""


