# Robust Build with Auto-Retry and Fix
# Run: .\BUILD_AND_FIX.ps1

Set-Location -Path "C:\Users\Administrator\Auto_Punch IDE"

$maxRetries = 3
$retryCount = 0
$buildSuccess = $false

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "ROBUST BUILD - AUTO RETRY AND FIX" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

while ($retryCount -lt $maxRetries -and -not $buildSuccess) {
    $retryCount++
    
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "BUILD ATTEMPT $retryCount of $maxRetries" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    
    # Refresh PATH
    $machinePath = [System.Environment]::GetEnvironmentVariable("Path","Machine")
    $userPath = [System.Environment]::GetEnvironmentVariable("Path","User")
    $env:Path = $machinePath + ";" + $userPath
    
    # Find Node.js
    Write-Host "[1/5] Finding Node.js..." -ForegroundColor Yellow
    $nodeExe = $null
    $npmExe = $null
    
    try {
        $nodeVersion = & node --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            $nodeExe = "node"
            $npmExe = "npm"
            Write-Host "  Node.js found: $nodeVersion" -ForegroundColor Green
        } else {
            throw "Not in PATH"
        }
    } catch {
        if (Test-Path "C:\Program Files\nodejs\node.exe") {
            $nodeExe = "C:\Program Files\nodejs\node.exe"
            $npmExe = "C:\Program Files\nodejs\npm.cmd"
            $env:Path = "C:\Program Files\nodejs;$env:Path"
            Write-Host "  Node.js found in Program Files" -ForegroundColor Green
        } else {
            Write-Host "  ERROR: Node.js not found!" -ForegroundColor Red
            exit 1
        }
    }
    Write-Host ""
    
    # Clean if retrying
    if ($retryCount -gt 1) {
        Write-Host "[2/5] Cleaning previous attempt..." -ForegroundColor Yellow
        Remove-Item -Path "dist" -Recurse -Force -ErrorAction SilentlyContinue
        Remove-Item -Path "node_modules\.cache" -Recurse -Force -ErrorAction SilentlyContinue
        Start-Sleep -Seconds 2
        Write-Host "  Cleaned" -ForegroundColor Green
        Write-Host ""
    }
    
    # Check dependencies
    Write-Host "[3/5] Checking dependencies..." -ForegroundColor Yellow
    if (-not (Test-Path "node_modules\electron")) {
        Write-Host "  Installing dependencies..." -ForegroundColor Yellow
        & $npmExe install
        if ($LASTEXITCODE -ne 0) {
            Write-Host "  WARNING: Installation had issues" -ForegroundColor Yellow
        } else {
            Write-Host "  Dependencies installed" -ForegroundColor Green
        }
    } else {
        Write-Host "  Dependencies ready" -ForegroundColor Green
    }
    Write-Host ""
    
    # Build
    Write-Host "[4/5] Building installer..." -ForegroundColor Yellow
    Write-Host "  This will take 10-15 minutes..." -ForegroundColor Gray
    Write-Host ""
    
    & $npmExe run build:exe
    $buildExitCode = $LASTEXITCODE
    
    Write-Host ""
    Write-Host "[5/5] Verifying build..." -ForegroundColor Yellow
    
    if ($buildExitCode -eq 0 -and (Test-Path "dist\Auto_Punch IDE Setup 1.0.0.exe")) {
        $exe = Get-Item "dist\Auto_Punch IDE Setup 1.0.0.exe"
        $sizeMB = [math]::Round($exe.Length/1MB, 2)
        Write-Host "  Build successful!" -ForegroundColor Green
        Write-Host "  Installer: $sizeMB MB" -ForegroundColor Green
        $buildSuccess = $true
    } else {
        Write-Host "  Build failed or installer not found" -ForegroundColor Red
        $buildSuccess = $false
        
        if ($retryCount -lt $maxRetries) {
            Write-Host ""
            Write-Host "Retrying in 5 seconds..." -ForegroundColor Yellow
            Start-Sleep -Seconds 5
        }
    }
}

# Final result
Write-Host ""
Write-Host "========================================" -ForegroundColor $(if ($buildSuccess) { "Green" } else { "Red" })
if ($buildSuccess) {
    Write-Host "BUILD SUCCESSFUL!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    
    $exe = Get-Item "dist\Auto_Punch IDE Setup 1.0.0.exe"
    Write-Host "Installer created:" -ForegroundColor Cyan
    Write-Host "  $($exe.FullName)" -ForegroundColor White
    Write-Host "  Size: $([math]::Round($exe.Length/1MB, 2)) MB" -ForegroundColor Gray
    Write-Host ""
    
    Write-Host "Opening dist folder..." -ForegroundColor Yellow
    Start-Sleep -Seconds 1
    explorer dist
} else {
    Write-Host "BUILD FAILED AFTER $maxRetries ATTEMPTS" -ForegroundColor Red
    Write-Host "========================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "Troubleshooting:" -ForegroundColor Yellow
    Write-Host "  1. Check Node.js installation" -ForegroundColor White
    Write-Host "  2. Check disk space (need ~2 GB)" -ForegroundColor White
    Write-Host "  3. Check internet connection" -ForegroundColor White
    Write-Host "  4. Try manual: npm run build:exe" -ForegroundColor White
}

Write-Host ""


