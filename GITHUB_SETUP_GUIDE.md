# GitHub Connection Setup Guide

## Quick Setup (Using Batch File)

1. **Run the setup script:**
   ```bash
   CONNECT_GITHUB.bat
   ```

2. **Follow the prompts:**
   - Enter your Git username
   - Enter your Git email
   - Enter your GitHub repository URL

## Manual Setup

### Step 1: Configure Git (if not already done)

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### Step 2: Initialize Git Repository (if not already done)

```bash
cd "C:\Users\Administrator\Auto_Punch IDE"
git init
```

### Step 3: Add GitHub Remote

**Option A: HTTPS (Easier, but requires token for private repos)**
```bash
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
```

**Option B: SSH (More secure, requires SSH key setup)**
```bash
git remote add origin git@github.com:YOUR_USERNAME/YOUR_REPO_NAME.git
```

### Step 4: Verify Connection

```bash
git remote -v
```

Should show:
```
origin  https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git (fetch)
origin  https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git (push)
```

### Step 5: Test Connection

```bash
git fetch origin
```

## Creating a New Repository on GitHub

If you don't have a repository yet:

1. **Go to GitHub:** https://github.com
2. **Click the "+" icon** in the top right
3. **Select "New repository"**
4. **Fill in details:**
   - Repository name: `Auto_Punch-IDE` (or your preferred name)
   - Description: "Standalone IDE with VS Code + Cursor features, powered by Auto_Punch Ai"
   - Choose **Private** (since you mentioned private repo)
   - **DO NOT** initialize with README, .gitignore, or license (we already have files)
5. **Click "Create repository"**
6. **Copy the repository URL** and use it in the setup

## Authentication for Private Repositories

### Option 1: Personal Access Token (HTTPS)

1. **Create a token:**
   - Go to: https://github.com/settings/tokens
   - Click "Generate new token" → "Generate new token (classic)"
   - Give it a name: "Auto_Punch IDE"
   - Select scopes: `repo` (full control of private repositories)
   - Click "Generate token"
   - **Copy the token** (you won't see it again!)

2. **Use token when pushing:**
   - When Git asks for password, use the token instead
   - Or configure Git Credential Manager to store it

### Option 2: SSH Keys (Recommended for frequent use)

1. **Generate SSH key (if you don't have one):**
   ```bash
   ssh-keygen -t ed25519 -C "your.email@example.com"
   ```

2. **Add SSH key to GitHub:**
   - Copy your public key: `type %USERPROFILE%\.ssh\id_ed25519.pub`
   - Go to: https://github.com/settings/keys
   - Click "New SSH key"
   - Paste the key and save

3. **Test SSH connection:**
   ```bash
   ssh -T git@github.com
   ```

## After Connection is Set Up

1. **Add all files:**
   ```bash
   git add .
   ```

2. **Create initial commit:**
   ```bash
   git commit -m "Initial commit: Auto_Punch IDE with AI code generation features"
   ```

3. **Push to GitHub:**
   ```bash
   git branch -M main
   git push -u origin main
   ```

## Troubleshooting

### "Repository not found" error
- Make sure the repository exists on GitHub
- Check the URL is correct
- Verify you have access (for private repos)

### "Authentication failed" error
- For HTTPS: Use Personal Access Token instead of password
- For SSH: Make sure SSH key is added to GitHub

### "Permission denied" error
- Check your GitHub account has access to the repository
- Verify SSH key is added to your GitHub account

## Need Help?

If you encounter issues, check:
- Git is installed: `git --version`
- Repository exists on GitHub
- Authentication is properly configured
- Network connection is working

