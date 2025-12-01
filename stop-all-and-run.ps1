# Stop All and Run - No Cancellation
# Run: .\stop-all-and-run.ps1

$ErrorActionPreference = "SilentlyContinue"

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "STOPPING ALL AND RUNNING BUILD" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

# Step 1: List and stop all interfering processes
Write-Host "[1/4] Listing and stopping processes..." -ForegroundColor Yellow
Write-Host ""

Write-Host "Python processes:" -ForegroundColor Cyan
$pythonProcs = Get-Process | Where-Object {$_.ProcessName -like "*python*"}
if ($pythonProcs) {
    $pythonProcs | ForEach-Object {
        Write-Host "  Stopping: $($_.ProcessName) (PID: $($_.Id))" -ForegroundColor Gray
        Stop-Process -Id $_.Id -Force -ErrorAction SilentlyContinue
    }
    Write-Host "  Stopped $($pythonProcs.Count) Python process(es)" -ForegroundColor Green
} else {
    Write-Host "  No Python processes" -ForegroundColor Gray
}

Write-Host ""
Write-Host "Node processes:" -ForegroundColor Cyan
$nodeProcs = Get-Process | Where-Object {$_.ProcessName -eq "node"} | Where-Object {$_.MainWindowTitle -notlike "*electron*"}
if ($nodeProcs) {
    $nodeProcs | ForEach-Object {
        Write-Host "  Stopping: node (PID: $($_.Id))" -ForegroundColor Gray
        Stop-Process -Id $_.Id -Force -ErrorAction SilentlyContinue
    }
    Write-Host "  Stopped $($nodeProcs.Count) Node process(es)" -ForegroundColor Green
} else {
    Write-Host "  No interfering Node processes" -ForegroundColor Gray
}

Start-Sleep -Seconds 2
Write-Host ""

# Step 2: Refresh PATH and verify Node.js
Write-Host "[2/4] Verifying Node.js..." -ForegroundColor Yellow
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
        throw "Node.js not in PATH"
    }
} catch {
    Write-Host "  Checking common locations..." -ForegroundColor Yellow
    $nodePaths = @(
        "C:\Program Files\nodejs\node.exe",
        "C:\Program Files (x86)\nodejs\node.exe",
        "$env:LOCALAPPDATA\Programs\nodejs\node.exe"
    )
    $found = $false
    foreach ($path in $nodePaths) {
        if (Test-Path $path) {
            $nodeDir = Split-Path $path
            $env:Path = "$nodeDir;$env:Path"
            Write-Host "  Found at: $path" -ForegroundColor Green
            $found = $true
            break
        }
    }
    if (-not $found) {
        Write-Host "  ERROR: Node.js not found!" -ForegroundColor Red
        Write-Host "  Please install Node.js first." -ForegroundColor Red
        exit 1
    }
}
Write-Host ""

# Step 3: Check dependencies
Write-Host "[3/4] Checking dependencies..." -ForegroundColor Yellow
if (Test-Path "node_modules\electron") {
    Write-Host "  Electron: Ready" -ForegroundColor Green
} else {
    Write-Host "  Installing dependencies..." -ForegroundColor Yellow
    & npm install
    if ($LASTEXITCODE -ne 0) {
        Write-Host "  WARNING: Installation had issues, but continuing..." -ForegroundColor Yellow
    }
}
Write-Host ""

# Step 4: Check build and build if needed
Write-Host "[4/4] Checking build..." -ForegroundColor Yellow
$installerPath = "dist\Auto_Punch IDE Setup 1.0.0.exe"

if (Test-Path $installerPath) {
    $exe = Get-Item $installerPath
    $sizeMB = [math]::Round($exe.Length/1MB, 2)
    Write-Host "  Installer found: $sizeMB MB" -ForegroundColor Green
} else {
    Write-Host "  Building installer (10-15 minutes)..." -ForegroundColor Yellow
    Write-Host "  This will run without cancellation..." -ForegroundColor Gray
    Write-Host ""
    
    & npm run build:exe
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host ""
        Write-Host "  ERROR: Build failed. Check errors above." -ForegroundColor Red
        exit 1
    }
    
    if (Test-Path $installerPath) {
        Write-Host ""
        Write-Host "  Build successful!" -ForegroundColor Green
    }
}
Write-Host ""

# Summary
Write-Host "========================================" -ForegroundColor Green
Write-Host "COMPLETE!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

if (Test-Path $installerPath) {
    $exe = Get-Item $installerPath
    $sizeMB = [math]::Round($exe.Length/1MB, 2)
    Write-Host "Installer: $($exe.FullName)" -ForegroundColor Cyan
    Write-Host "Size: $sizeMB MB" -ForegroundColor Gray
}

Write-Host ""
Write-Host "Opening dist folder..." -ForegroundColor Yellow
Start-Sleep -Seconds 1
explorer dist

Write-Host ""
