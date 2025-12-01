# Setup Remote Server Configuration
# Run: .\setup-remote-server.ps1

Set-Location -Path "C:\Users\Administrator\Auto_Punch IDE"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "REMOTE SERVER SETUP" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Choose deployment option:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Railway (Recommended - Easy deployment)" -ForegroundColor Green
Write-Host "2. Supabase (Backend-as-a-Service)" -ForegroundColor Green
Write-Host "3. cPanel (Traditional hosting)" -ForegroundColor Green
Write-Host "4. Local Server (Development)" -ForegroundColor Gray
Write-Host ""

$choice = Read-Host "Enter choice (1-4)"

switch ($choice) {
    "1" {
        Write-Host ""
        Write-Host "Railway Setup:" -ForegroundColor Cyan
        $railwayUrl = Read-Host "Enter your Railway app URL (e.g., https://your-app.railway.app)"
        
        $config = @{
            serverUrl = $railwayUrl
            useLocalServer = $false
            railwayUrl = $railwayUrl
            supabaseUrl = ""
            production = $true
        } | ConvertTo-Json
        
        $config | Out-File "electron\config.json" -Encoding UTF8
        Write-Host "✓ Railway configuration saved!" -ForegroundColor Green
        Write-Host ""
        Write-Host "Next steps:" -ForegroundColor Yellow
        Write-Host "  1. Deploy to Railway (see DEPLOYMENT_GUIDE.md)" -ForegroundColor Gray
        Write-Host "  2. Rebuild Electron app: .\fix-and-rebuild.ps1" -ForegroundColor Gray
    }
    "2" {
        Write-Host ""
        Write-Host "Supabase Setup:" -ForegroundColor Cyan
        $supabaseUrl = Read-Host "Enter your Supabase project URL"
        $supabaseKey = Read-Host "Enter your Supabase anon key"
        
        # Create .env file
        $envContent = @"
SUPABASE_URL=$supabaseUrl
SUPABASE_KEY=$supabaseKey
FLASK_ENV=production
PORT=5001
HOST=0.0.0.0
"@
        $envContent | Out-File ".env" -Encoding UTF8
        
        $config = @{
            serverUrl = $supabaseUrl
            useLocalServer = $false
            railwayUrl = ""
            supabaseUrl = $supabaseUrl
            production = $true
        } | ConvertTo-Json
        
        $config | Out-File "electron\config.json" -Encoding UTF8
        Write-Host "✓ Supabase configuration saved!" -ForegroundColor Green
        Write-Host ""
        Write-Host "Next steps:" -ForegroundColor Yellow
        Write-Host "  1. Install supabase: pip install supabase" -ForegroundColor Gray
        Write-Host "  2. Deploy backend to Railway/cPanel" -ForegroundColor Gray
        Write-Host "  3. Rebuild Electron app: .\fix-and-rebuild.ps1" -ForegroundColor Gray
    }
    "3" {
        Write-Host ""
        Write-Host "cPanel Setup:" -ForegroundColor Cyan
        $cpanelUrl = Read-Host "Enter your cPanel domain URL (e.g., https://yourdomain.com)"
        
        $config = @{
            serverUrl = $cpanelUrl
            useLocalServer = $false
            railwayUrl = ""
            supabaseUrl = ""
            production = $true
        } | ConvertTo-Json
        
        $config | Out-File "electron\config.json" -Encoding UTF8
        Write-Host "✓ cPanel configuration saved!" -ForegroundColor Green
        Write-Host ""
        Write-Host "Next steps:" -ForegroundColor Yellow
        Write-Host "  1. Upload files to cPanel (see DEPLOYMENT_GUIDE.md)" -ForegroundColor Gray
        Write-Host "  2. Setup Python app in cPanel" -ForegroundColor Gray
        Write-Host "  3. Rebuild Electron app: .\fix-and-rebuild.ps1" -ForegroundColor Gray
    }
    "4" {
        Write-Host ""
        Write-Host "Local Server (Development):" -ForegroundColor Cyan
        
        $config = @{
            serverUrl = "http://localhost:5001"
            useLocalServer = $true
            railwayUrl = ""
            supabaseUrl = ""
            production = $false
        } | ConvertTo-Json
        
        $config | Out-File "electron\config.json" -Encoding UTF8
        Write-Host "✓ Local server configuration saved!" -ForegroundColor Green
    }
    default {
        Write-Host "Invalid choice!" -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "Configuration Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "See DEPLOYMENT_GUIDE.md for deployment instructions" -ForegroundColor Cyan
Write-Host ""


