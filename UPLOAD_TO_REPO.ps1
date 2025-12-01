# Upload Full Project to Specific Repository with Token Auth
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  UPLOAD TO: Auto-ai-sorce-snd-exe" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

Set-Location "C:\Users\Administrator\Auto_Punch IDE"

$repoUrl = "https://github.com/forcer-smg/Auto-ai-sorce-snd-exe-.git"
$repoName = "Auto-ai-sorce-snd-exe-"

# Check Git
$gitAvailable = Get-Command git -ErrorAction SilentlyContinue
if (-not $gitAvailable) {
    Write-Host "[!] Git is not installed" -ForegroundColor Red
    Write-Host "Download from: https://git-scm.com/download/win" -ForegroundColor Yellow
    exit 1
}

Write-Host "[+] Git found" -ForegroundColor Green

# Get Personal Access Token
Write-Host ""
Write-Host "============================================================" -ForegroundColor Yellow
Write-Host "  AUTHENTICATION SETUP" -ForegroundColor Yellow
Write-Host "============================================================" -ForegroundColor Yellow
Write-Host ""
Write-Host "You need a GitHub Personal Access Token" -ForegroundColor Cyan
Write-Host ""
Write-Host "If you don't have one:" -ForegroundColor Yellow
Write-Host "1. Go to: https://github.com/settings/tokens" -ForegroundColor White
Write-Host "2. Click 'Generate new token' -> 'Generate new token (classic)'" -ForegroundColor White
Write-Host "3. Name: 'Auto_Punch IDE Upload'" -ForegroundColor White
Write-Host "4. Scopes: Check 'repo' (full control of private repositories)" -ForegroundColor White
Write-Host "5. Click 'Generate token'" -ForegroundColor White
Write-Host "6. COPY THE TOKEN (you won't see it again!)" -ForegroundColor Red
Write-Host ""

$token = Read-Host "Enter your GitHub Personal Access Token" -AsSecureString
$tokenPlain = [Runtime.InteropServices.Marshal]::PtrToStringAuto(
    [Runtime.InteropServices.Marshal]::SecureStringToBSTR($token)
)

if ([string]::IsNullOrWhiteSpace($tokenPlain)) {
    Write-Host "[!] Token is required" -ForegroundColor Red
    exit 1
}

# Configure Git to use token
Write-Host ""
Write-Host "[~] Configuring Git credentials..." -ForegroundColor Yellow

# Extract username from token or ask
$username = Read-Host "Enter your GitHub username (or press Enter to use 'forcer-smg')"
if ([string]::IsNullOrWhiteSpace($username)) {
    $username = "forcer-smg"
}

# Build URL with token
$authenticatedUrl = "https://${username}:${tokenPlain}@github.com/forcer-smg/Auto-ai-sorce-snd-exe-.git"

# Check if already a git repo
$isGitRepo = Test-Path ".git"

if ($isGitRepo) {
    Write-Host "[+] Already a git repository" -ForegroundColor Green
    
    # Check current remote
    $currentRemote = git remote get-url origin 2>$null
    if ($currentRemote) {
        Write-Host "[+] Current remote: $currentRemote" -ForegroundColor Cyan
        Write-Host ""
        $updateRemote = Read-Host "Update remote to use token? (Y/n)"
        if ($updateRemote -eq "" -or $updateRemote -eq "Y" -or $updateRemote -eq "y") {
            git remote set-url origin $authenticatedUrl
            Write-Host "[+] Remote updated with token authentication" -ForegroundColor Green
        }
    } else {
        git remote add origin $authenticatedUrl
        Write-Host "[+] Remote added with token authentication" -ForegroundColor Green
    }
} else {
    Write-Host "[~] Initializing git repository..." -ForegroundColor Yellow
    git init
    git remote add origin $authenticatedUrl
    Write-Host "[+] Repository initialized" -ForegroundColor Green
}

# Update .gitignore to allow releases folder
Write-Host ""
Write-Host "[~] Updating .gitignore..." -ForegroundColor Yellow
$gitignoreContent = Get-Content .gitignore -Raw -ErrorAction SilentlyContinue
if (-not $gitignoreContent) {
    $gitignoreContent = ""
}

if ($gitignoreContent -notmatch "!releases/") {
    $gitignoreContent += "`n# Allow releases folder`n!releases/`n!releases/**/*.exe`n"
    Set-Content -Path ".gitignore" -Value $gitignoreContent
    Write-Host "[+] Updated .gitignore" -ForegroundColor Green
}

# Create releases directory and copy EXE
Write-Host ""
Write-Host "[~] Preparing releases..." -ForegroundColor Yellow
$releasesDir = "releases"
if (-not (Test-Path $releasesDir)) {
    New-Item -ItemType Directory -Path $releasesDir | Out-Null
}

# Find and copy EXE
$exePath = "dist\Auto_Punch IDE Setup 1.0.0.exe"
$unpackedExe = "dist\win-unpacked\Auto_Punch IDE.exe"

if (Test-Path $exePath) {
    $exeName = "Auto_Punch IDE Setup 1.0.0.exe"
    Copy-Item -Path $exePath -Destination "$releasesDir\$exeName" -Force
    Write-Host "[+] Copied installer to releases folder" -ForegroundColor Green
} elseif (Test-Path $unpackedExe) {
    $exeName = "Auto_Punch IDE.exe"
    Copy-Item -Path $unpackedExe -Destination "$releasesDir\$exeName" -Force
    Write-Host "[+] Copied executable to releases folder" -ForegroundColor Green
} else {
    Write-Host "[!] No executable found. Will upload source code only." -ForegroundColor Yellow
    Write-Host "    You can build and add the EXE later." -ForegroundColor Yellow
}

# Create/Update README
if (-not (Test-Path "README.md")) {
    Write-Host ""
    Write-Host "[~] Creating README.md..." -ForegroundColor Yellow
    $readmeContent = @"
# Auto_Punch IDE Desktop

Full-featured IDE with VS Code + Cursor features, powered by Auto_Punch Ai.

## Features

- ✅ Full IDE with VS Code + Cursor features
- ✅ Auto_Punch Ai integration
- ✅ RedTeam Toolkit (138 tools)
- ✅ Telegram integration (separate repo)
- ✅ Settings sync (Supabase)
- ✅ Desktop app registration

## Releases

Latest release: [releases/](./releases/)

## Development

### Prerequisites

- Python 3.11 or later
- Node.js and npm
- Git

### Setup

\`\`\`powershell
# Clone repository
git clone https://github.com/forcer-smg/Auto-ai-sorce-snd-exe-.git
cd Auto-ai-sorce-snd-exe-

# Install Python dependencies
pip install -r requirements.txt

# Install Node dependencies
npm install

# Install tool dependencies
pip install -r "RedTeam-Tools\365-Stealer\requirements.txt"
cd "RedTeam-Tools\requests-ip-rotator"
pip install -e .
cd ..\..
\`\`\`

### Build

\`\`\`powershell
# Build executable
npm run build:exe

# Copy to releases folder
Copy-Item "dist\Auto_Punch IDE Setup 1.0.0.exe" "releases\"
\`\`\`

### Update Release

\`\`\`powershell
# After building, copy EXE to releases folder
Copy-Item "dist\Auto_Punch IDE Setup 1.0.0.exe" "releases\"

# Commit and push
git add .
git commit -m "Update release v1.0.0"
git push origin main
\`\`\`

## Configuration

### Environment Variables

- \`TELEGRAM_BOT_TOKEN\` - Telegram bot token (for notifications)
- \`TELEGRAM_CHAT_ID\` - Telegram chat ID
- \`SUPABASE_URL\` - Supabase project URL
- \`SUPABASE_KEY\` - Supabase API key

## Project Structure

\`\`\`
Auto-ai-sorce-snd-exe-/
├── app.py                 # Flask backend
├── electron/             # Electron main process
├── static/               # Frontend assets
├── templates/            # HTML templates
├── RedTeam-Tools/        # Security tools
├── releases/             # Built executables
└── dist/                 # Build output (gitignored)
\`\`\`

## Notes

- Telegram integration is in a separate repository
- First run may take time to initialize Auto_Punch Ai components
- Ensure Python is in your PATH
- Private repository - for development and releases only

## License

Private - All rights reserved
"@
    Set-Content -Path "README.md" -Value $readmeContent
    Write-Host "[+] Created README.md" -ForegroundColor Green
}

# Create .gitattributes if needed
if (-not (Test-Path ".gitattributes")) {
    $gitattributes = @"
* text=auto
*.bat text eol=crlf
*.ps1 text eol=crlf
*.py text eol=lf
*.js text eol=lf
*.json text eol=lf
*.md text eol=lf
"@
    Set-Content -Path ".gitattributes" -Value $gitattributes
    Write-Host "[+] Created .gitattributes" -ForegroundColor Green
}

# Stage all files
Write-Host ""
Write-Host "[~] Staging files..." -ForegroundColor Yellow
git add .

# Show what will be committed
Write-Host ""
Write-Host "Files to be committed:" -ForegroundColor Cyan
git status --short | Select-Object -First 20
$totalFiles = (git status --short | Measure-Object).Count
if ($totalFiles -gt 20) {
    Write-Host "... and $($totalFiles - 20) more files" -ForegroundColor Gray
}

Write-Host ""
$commitMessage = Read-Host "Commit message (or press Enter for default)"
if ([string]::IsNullOrWhiteSpace($commitMessage)) {
    $commitMessage = "Initial commit - Auto_Punch IDE v1.0.0 with full source code and EXE"
}

Write-Host ""
Write-Host "[~] Committing changes..." -ForegroundColor Yellow
git commit -m $commitMessage

if ($LASTEXITCODE -eq 0) {
    Write-Host "[+] Changes committed" -ForegroundColor Green
    
    Write-Host ""
    Write-Host "[~] Pushing to GitHub (using token authentication)..." -ForegroundColor Yellow
    
    # Determine branch
    $branch = git branch --show-current
    if (-not $branch) {
        $branch = "main"
        git branch -M main
    }
    
    # Push using the authenticated URL
    git push -u origin $branch
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "============================================================" -ForegroundColor Green
        Write-Host "  SUCCESSFULLY UPLOADED TO GITHUB" -ForegroundColor Green
        Write-Host "============================================================" -ForegroundColor Green
        Write-Host ""
        Write-Host "Repository: https://github.com/forcer-smg/Auto-ai-sorce-snd-exe-" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "✅ Full source code uploaded" -ForegroundColor Green
        Write-Host "✅ EXE uploaded to releases folder" -ForegroundColor Green
        Write-Host ""
        Write-Host "Next steps:" -ForegroundColor Yellow
        Write-Host "1. Clone on another machine: git clone $repoUrl" -ForegroundColor White
        Write-Host "2. Make edits, build, and push updates" -ForegroundColor White
        Write-Host "3. Use .\QUICK_UPDATE.ps1 for daily updates" -ForegroundColor White
        Write-Host ""
        Write-Host "Note: Token is stored in remote URL. For security, consider:" -ForegroundColor Yellow
        Write-Host "  - Using SSH keys instead" -ForegroundColor White
        Write-Host "  - Or using Git Credential Manager" -ForegroundColor White
    } else {
        Write-Host ""
        Write-Host "[!] Push failed. Check:" -ForegroundColor Red
        Write-Host "   - Token is valid and has 'repo' scope" -ForegroundColor White
        Write-Host "   - Repository exists and you have access" -ForegroundColor White
        Write-Host "   - Internet connection" -ForegroundColor White
    }
} else {
    Write-Host ""
    Write-Host "[!] Commit failed" -ForegroundColor Red
}

# Clear token from memory
$tokenPlain = $null
$token = $null

Write-Host ""
Read-Host "Press Enter to exit"

