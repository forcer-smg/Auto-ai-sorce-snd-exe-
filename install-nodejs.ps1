# Auto_Punch IDE - Node.js Installation Script
# This script downloads and installs Node.js LTS automatically

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Node.js Installation for Auto_Punch IDE" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Node.js is already installed
$nodeCheck = Get-Command node -ErrorAction SilentlyContinue
if ($nodeCheck) {
    $nodeVersion = node --version
    Write-Host "Node.js is already installed: $nodeVersion" -ForegroundColor Green
    Write-Host "Skipping installation." -ForegroundColor Yellow
    exit 0
}

Write-Host "Node.js not found. Starting installation..." -ForegroundColor Yellow
Write-Host ""

# Node.js LTS download URL (update version as needed)
$nodeVersion = "20.11.0"
$nodeUrl = "https://nodejs.org/dist/v$nodeVersion/node-v$nodeVersion-x64.msi"
$installerPath = "$env:TEMP\nodejs-installer.msi"

Write-Host "Downloading Node.js LTS v$nodeVersion..." -ForegroundColor Yellow
Write-Host "URL: $nodeUrl" -ForegroundColor Gray

try {
    # Download Node.js installer
    $ProgressPreference = 'SilentlyContinue'
    Invoke-WebRequest -Uri $nodeUrl -OutFile $installerPath -UseBasicParsing
    
    if (Test-Path $installerPath) {
        Write-Host "Download complete!" -ForegroundColor Green
        Write-Host ""
        Write-Host "Installing Node.js..." -ForegroundColor Yellow
        Write-Host "This may take a few minutes. Please wait..." -ForegroundColor Gray
        
        # Install Node.js silently
        $installArgs = "/i `"$installerPath`" /quiet /norestart ADDLOCAL=ALL"
        Start-Process -FilePath "msiexec.exe" -ArgumentList $installArgs -Wait -NoNewWindow
        
        Write-Host ""
        Write-Host "Installation complete!" -ForegroundColor Green
        Write-Host ""
        Write-Host "Refreshing environment variables..." -ForegroundColor Yellow
        
        # Refresh PATH
        $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
        
        # Clean up installer
        Remove-Item $installerPath -Force -ErrorAction SilentlyContinue
        
        Write-Host ""
        Write-Host "Verifying installation..." -ForegroundColor Yellow
        
        # Wait a moment for PATH to update
        Start-Sleep -Seconds 2
        
        # Check if Node.js is now available
        $nodeCheck = Get-Command node -ErrorAction SilentlyContinue
        if ($nodeCheck) {
            $nodeVersion = node --version
            $npmVersion = npm --version
            Write-Host ""
            Write-Host "========================================" -ForegroundColor Green
            Write-Host "Node.js installed successfully!" -ForegroundColor Green
            Write-Host "========================================" -ForegroundColor Green
            Write-Host "Node.js: $nodeVersion" -ForegroundColor Green
            Write-Host "npm: $npmVersion" -ForegroundColor Green
            Write-Host ""
            Write-Host "You may need to restart PowerShell for PATH to fully update." -ForegroundColor Yellow
            Write-Host "Or run: refreshenv" -ForegroundColor Yellow
        } else {
            Write-Host ""
            Write-Host "Node.js installed but not in PATH yet." -ForegroundColor Yellow
            Write-Host "Please restart PowerShell and run: node --version" -ForegroundColor Yellow
        }
    } else {
        Write-Host "Download failed!" -ForegroundColor Red
        Write-Host "Please download manually from: https://nodejs.org/" -ForegroundColor Yellow
    }
} catch {
    Write-Host ""
    Write-Host "Automatic installation failed: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install Node.js manually:" -ForegroundColor Yellow
    Write-Host "1. Visit: https://nodejs.org/" -ForegroundColor White
    Write-Host "2. Download Windows Installer (.msi)" -ForegroundColor White
    Write-Host "3. Run installer and check 'Add to PATH'" -ForegroundColor White
    Write-Host "4. Restart PowerShell" -ForegroundColor White
    Write-Host "5. Run: npm install" -ForegroundColor White
}


