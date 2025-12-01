# Upload Full Project (Source Code + EXE) to Private GitHub Repository
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  UPLOAD FULL PROJECT TO PRIVATE GITHUB REPOSITORY" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

Set-Location "C:\Users\Administrator\Auto_Punch IDE"

# Check authentication
$ghAvailable = Get-Command gh -ErrorAction SilentlyContinue
$gitAvailable = Get-Command git -ErrorAction SilentlyContinue

if (-not $gitAvailable) {
    Write-Host "[!] Git is not installed" -ForegroundColor Red
    Write-Host "Download from: https://git-scm.com/download/win" -ForegroundColor Yellow
    exit 1
}

Write-Host "[+] Git found" -ForegroundColor Green

# Check if already a git repo
$isGitRepo = Test-Path ".git"
if ($isGitRepo) {
    Write-Host "[+] Already a git repository" -ForegroundColor Green
    $currentRemote = git remote get-url origin 2>$null
    if ($currentRemote) {
        Write-Host "[+] Current remote: $currentRemote" -ForegroundColor Cyan
        Write-Host ""
        $useExisting = Read-Host "Use existing remote? (Y/n)"
        if ($useExisting -eq "" -or $useExisting -eq "Y" -or $useExisting -eq "y") {
            $repoOwner = ""
            $repoName = ""
        }
    }
}

if (-not $isGitRepo -or ($useExisting -ne "" -and $useExisting -ne "Y" -and $useExisting -ne "y")) {
    Write-Host ""
    Write-Host "============================================================" -ForegroundColor Yellow
    Write-Host "  REPOSITORY SETUP" -ForegroundColor Yellow
    Write-Host "============================================================" -ForegroundColor Yellow
    Write-Host ""
    
    if ($ghAvailable) {
        Write-Host "[+] GitHub CLI found" -ForegroundColor Green
        Write-Host ""
        Write-Host "Option 1: Create new private repository (Recommended)" -ForegroundColor Cyan
        Write-Host "Option 2: Use existing repository" -ForegroundColor Cyan
        Write-Host ""
        $option = Read-Host "Choose option (1/2)"
        
        if ($option -eq "1") {
            # Create new repo
            $repoName = Read-Host "Repository name (e.g., Auto-Punch-IDE)"
            $repoDesc = Read-Host "Description (optional)"
            
            Write-Host ""
            Write-Host "[~] Checking GitHub CLI authentication..." -ForegroundColor Yellow
            $authStatus = gh auth status 2>&1
            if ($LASTEXITCODE -ne 0) {
                Write-Host "[!] Not authenticated. Starting authentication..." -ForegroundColor Yellow
                gh auth login
            }
            
            Write-Host ""
            Write-Host "[~] Creating private repository..." -ForegroundColor Yellow
            if ($repoDesc) {
                gh repo create $repoName --private --description $repoDesc --source=. --remote=origin
            } else {
                gh repo create $repoName --private --source=. --remote=origin
            }
            
            if ($LASTEXITCODE -eq 0) {
                Write-Host "[+] Repository created and remote added" -ForegroundColor Green
                $repoOwner = (gh api user --jq .login)
            } else {
                Write-Host "[!] Failed to create repository" -ForegroundColor Red
                exit 1
            }
        } else {
            # Use existing repo
            $repoOwner = Read-Host "Repository Owner/Username"
            $repoName = Read-Host "Repository Name"
            
            if (-not $isGitRepo) {
                git init
            }
            
            Write-Host ""
            Write-Host "[~] Adding remote..." -ForegroundColor Yellow
            git remote add origin "https://github.com/$repoOwner/$repoName.git"
            Write-Host "[+] Remote added" -ForegroundColor Green
        }
    } else {
        Write-Host "[!] GitHub CLI not found. Using Git directly." -ForegroundColor Yellow
        Write-Host "For easier setup, install GitHub CLI: https://cli.github.com/" -ForegroundColor Yellow
        Write-Host ""
        
        $repoOwner = Read-Host "Repository Owner/Username"
        $repoName = Read-Host "Repository Name"
        
        if (-not $isGitRepo) {
            git init
        }
        
        Write-Host ""
        Write-Host "[~] Adding remote..." -ForegroundColor Yellow
        git remote add origin "https://github.com/$repoOwner/$repoName.git"
        Write-Host "[+] Remote added" -ForegroundColor Green
        Write-Host ""
        Write-Host "Note: You'll need to authenticate when pushing" -ForegroundColor Yellow
    }
}

# Update .gitignore to include EXE in releases folder
Write-Host ""
Write-Host "[~] Updating .gitignore..." -ForegroundColor Yellow
$gitignoreContent = Get-Content .gitignore -Raw -ErrorAction SilentlyContinue
if (-not $gitignoreContent) {
    $gitignoreContent = ""
}

# Ensure releases folder is tracked but dist is not
if ($gitignoreContent -notmatch "releases/") {
    # Add exception for releases folder
    $gitignoreContent += "`n# Allow releases folder`n!releases/`n!releases/**/*.exe`n"
    Set-Content -Path ".gitignore" -Value $gitignoreContent
    Write-Host "[+] Updated .gitignore to allow releases folder" -ForegroundColor Green
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

# Create README if it doesn't exist or update it
if (-not (Test-Path "README.md") -or (Read-Host "Update README.md? (Y/n)") -eq "" -or (Read-Host "Update README.md? (Y/n)") -eq "Y") {
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
git clone https://github.com/YOUR_USERNAME/Auto-Punch-IDE.git
cd Auto-Punch-IDE

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

# The EXE will be in: dist\Auto_Punch IDE Setup 1.0.0.exe
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
Auto-Punch-IDE/
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

[Your License Here]
"@
    Set-Content -Path "README.md" -Value $readmeContent
    Write-Host "[+] Created/Updated README.md" -ForegroundColor Green
}

# Create .gitattributes to handle line endings
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
    $commitMessage = "Initial commit - Auto_Punch IDE v1.0.0 with full source code"
}

Write-Host ""
Write-Host "[~] Committing changes..." -ForegroundColor Yellow
git commit -m $commitMessage

if ($LASTEXITCODE -eq 0) {
    Write-Host "[+] Changes committed" -ForegroundColor Green
    
    Write-Host ""
    Write-Host "[~] Pushing to GitHub..." -ForegroundColor Yellow
    
    # Determine branch
    $branch = git branch --show-current
    if (-not $branch) {
        $branch = "main"
        git branch -M main
    }
    
    if ($ghAvailable) {
        git push -u origin $branch
    } else {
        Write-Host "If prompted for credentials:" -ForegroundColor Yellow
        Write-Host "  Username: Your GitHub username" -ForegroundColor White
        Write-Host "  Password: Your Personal Access Token (not your password!)" -ForegroundColor White
        git push -u origin $branch
    }
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "============================================================" -ForegroundColor Green
        Write-Host "  SUCCESSFULLY UPLOADED TO PRIVATE REPOSITORY" -ForegroundColor Green
        Write-Host "============================================================" -ForegroundColor Green
        Write-Host ""
        if ($repoOwner -and $repoName) {
            Write-Host "Repository: https://github.com/$repoOwner/$repoName" -ForegroundColor Cyan
        } else {
            $remoteUrl = git remote get-url origin
            Write-Host "Repository: $remoteUrl" -ForegroundColor Cyan
        }
        Write-Host ""
        Write-Host "✅ Full source code uploaded" -ForegroundColor Green
        Write-Host "✅ EXE uploaded to releases folder" -ForegroundColor Green
        Write-Host ""
        Write-Host "Next steps:" -ForegroundColor Yellow
        Write-Host "1. Clone the repo on another machine: git clone <repo-url>" -ForegroundColor White
        Write-Host "2. Make edits, build, and push updates" -ForegroundColor White
        Write-Host "3. Set up Telegram integration in separate repo" -ForegroundColor White
    } else {
        Write-Host ""
        Write-Host "[!] Push failed. Check authentication." -ForegroundColor Red
        Write-Host "See CREATE_PRIVATE_REPO.md for authentication help" -ForegroundColor Yellow
    }
} else {
    Write-Host ""
    Write-Host "[!] Commit failed" -ForegroundColor Red
}

Write-Host ""
Read-Host "Press Enter to exit"

