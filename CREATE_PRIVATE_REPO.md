# Create and Connect Private GitHub Repository

## Step 1: Create Private Repository on GitHub

### Via GitHub Web Interface

1. **Go to GitHub:**
   - Visit: https://github.com/new
   - Or click the "+" icon → "New repository"

2. **Fill in details:**
   - **Repository name:** `Auto-Punch-IDE-Releases` (or your preferred name)
   - **Description:** `Auto_Punch IDE Desktop Application Releases`
   - **Visibility:** Select **🔒 Private** (important!)
   - **Initialize:** 
     - ✅ Add a README file (optional)
     - ❌ Don't add .gitignore (we have one)
     - ❌ Don't choose a license (or add one if needed)

3. **Click "Create repository"**

### Via GitHub CLI

```powershell
# Install GitHub CLI first: https://cli.github.com/
gh auth login

# Create private repository
gh repo create Auto-Punch-IDE-Releases `
  --private `
  --description "Auto_Punch IDE Desktop Application Releases" `
  --clone
```

## Step 2: Connect to Private Repository

### Option A: Clone Existing Private Repo

```powershell
# Using HTTPS (requires authentication)
git clone https://github.com/YOUR_USERNAME/Auto-Punch-IDE-Releases.git

# Using SSH (requires SSH key setup)
git clone git@github.com:YOUR_USERNAME/Auto-Punch-IDE-Releases.git
```

### Option B: Add Remote to Existing Local Repo

```powershell
cd "C:\Users\Administrator\Auto_Punch IDE"

# Add remote
git remote add releases https://github.com/YOUR_USERNAME/Auto-Punch-IDE-Releases.git

# Verify
git remote -v
```

### Option C: Initialize New Repo and Connect

```powershell
cd "C:\Users\Administrator\Auto_Punch IDE"

# Initialize git (if not already)
git init

# Add remote
git remote add origin https://github.com/YOUR_USERNAME/Auto-Punch-IDE-Releases.git

# Add files
git add .

# Commit
git commit -m "Initial commit - Auto_Punch IDE v1.0.0"

# Push
git branch -M main
git push -u origin main
```

## Step 3: Authentication for Private Repo

### Option 1: Personal Access Token (HTTPS)

1. **Create Token:**
   - Go to: https://github.com/settings/tokens
   - Click "Generate new token" → "Generate new token (classic)"
   - Name: `Auto_Punch IDE Upload`
   - Scopes: Check `repo` (full control of private repositories)
   - Click "Generate token"
   - **Copy the token immediately** (you won't see it again!)

2. **Use Token:**
   ```powershell
   # When prompted for password, use the token instead
   git push origin main
   # Username: YOUR_USERNAME
   # Password: YOUR_TOKEN
   ```

3. **Store Credentials (Windows):**
   ```powershell
   # Git will use Windows Credential Manager
   # Or configure Git Credential Manager
   git config --global credential.helper manager-core
   ```

### Option 2: SSH Key (Recommended)

1. **Generate SSH Key:**
   ```powershell
   # Check if you have existing SSH key
   Test-Path ~\.ssh\id_rsa.pub

   # If not, generate new key
   ssh-keygen -t ed25519 -C "your_email@example.com"
   # Press Enter to accept default location
   # Enter passphrase (optional but recommended)
   ```

2. **Add SSH Key to GitHub:**
   ```powershell
   # Copy public key
   Get-Content ~\.ssh\id_ed25519.pub | Set-Clipboard
   # Or: cat ~/.ssh/id_ed25519.pub
   ```

   - Go to: https://github.com/settings/keys
   - Click "New SSH key"
   - Title: `Auto_Punch IDE Upload`
   - Key: Paste the copied key
   - Click "Add SSH key"

3. **Test SSH Connection:**
   ```powershell
   ssh -T git@github.com
   # Should see: "Hi USERNAME! You've successfully authenticated..."
   ```

4. **Use SSH URL:**
   ```powershell
   git remote set-url origin git@github.com:YOUR_USERNAME/Auto-Punch-IDE-Releases.git
   ```

### Option 3: GitHub CLI (Easiest)

```powershell
# Install: https://cli.github.com/
# Authenticate
gh auth login

# This handles authentication automatically
gh repo clone YOUR_USERNAME/Auto-Punch-IDE-Releases
```

## Step 4: Upload EXE to Private Repo

### Automated Script (Updated)

```powershell
.\UPLOAD_EXE_TO_PRIVATE_REPO.ps1
```

### Manual Upload

1. **Copy EXE to repo:**
   ```powershell
   cd "C:\Users\Administrator\Auto_Punch IDE"
   git clone https://github.com/YOUR_USERNAME/Auto-Punch-IDE-Releases.git temp-repo
   Copy-Item "dist\Auto_Punch IDE Setup 1.0.0.exe" "temp-repo\releases\"
   cd temp-repo
   git add .
   git commit -m "Add Auto_Punch IDE v1.0.0 release"
   git push origin main
   cd ..
   Remove-Item -Recurse -Force temp-repo
   ```

2. **Or create GitHub Release:**
   - Go to: `https://github.com/YOUR_USERNAME/Auto-Punch-IDE-Releases/releases/new`
   - Create release with tag `v1.0.0`
   - Upload the EXE as release asset

## Quick Setup Script

Run this to set everything up:

```powershell
# Set these variables
$repoOwner = "YOUR_USERNAME"
$repoName = "Auto-Punch-IDE-Releases"

# Create repo (requires GitHub CLI)
gh repo create $repoName --private --description "Auto_Punch IDE Releases"

# Clone
gh repo clone $repoOwner/$repoName

# Copy EXE
Copy-Item "dist\Auto_Punch IDE Setup 1.0.0.exe" "$repoName\releases\"

# Commit and push
cd $repoName
git add .
git commit -m "Add Auto_Punch IDE v1.0.0"
git push origin main
```

## Troubleshooting

### Authentication Failed
- **HTTPS:** Use Personal Access Token instead of password
- **SSH:** Check SSH key is added to GitHub
- **GitHub CLI:** Run `gh auth login` again

### Permission Denied
- Check repository is private and you have access
- Verify authentication method
- Check token/SSH key has `repo` scope

### Repository Not Found
- Verify repository name and owner
- Check repository visibility (private repos need authentication)
- Ensure you're authenticated

## Security Notes

- ✅ Private repos are only visible to you and collaborators
- ✅ Use Personal Access Tokens with minimal required scopes
- ✅ Use SSH keys with passphrases
- ✅ Don't commit tokens or keys to the repository
- ✅ Use environment variables for sensitive data

