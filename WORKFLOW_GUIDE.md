# Development Workflow Guide

## Repository Structure

### Main Repository (This Repo)
- **Purpose:** Full source code + releases
- **Contains:**
  - All source code
  - Configuration files
  - Built executables (in `releases/` folder)
  - Documentation

### Telegram Integration Repository (Separate)
- **Purpose:** Telegram bot and webhook handlers
- **Contains:**
  - Telegram bot code
  - Railway deployment config
  - Supabase integration
  - Webhook handlers

## Development Workflow

### 1. Clone and Setup

```powershell
# Clone the repository
git clone https://github.com/YOUR_USERNAME/Auto-Punch-IDE.git
cd Auto-Punch-IDE

# Install dependencies
pip install -r requirements.txt
npm install

# Install tool dependencies
pip install -r "RedTeam-Tools\365-Stealer\requirements.txt"
cd "RedTeam-Tools\requests-ip-rotator"
pip install -e .
cd ..\..
```

### 2. Make Changes

Edit any files as needed:
- `app.py` - Backend changes
- `static/js/ide.js` - Frontend changes
- `electron/main.js` - Electron changes
- Any other source files

### 3. Test Changes

```powershell
# Run in development mode
python app.py

# Or test Electron app
npm start
```

### 4. Build New Release

```powershell
# Build executable
npm run build:exe

# Copy to releases folder
Copy-Item "dist\Auto_Punch IDE Setup 1.0.0.exe" "releases\Auto_Punch IDE Setup 1.0.0.exe"
```

### 5. Commit and Push

```powershell
# Stage all changes
git add .

# Commit
git commit -m "Description of changes"

# Push
git push origin main
```

### 6. Update Release (Optional)

If you built a new EXE:

```powershell
# Copy new EXE to releases
Copy-Item "dist\Auto_Punch IDE Setup 1.0.0.exe" "releases\"

# Commit and push
git add releases/
git commit -m "Update release v1.0.1"
git push origin main
```

## Quick Commands

### Daily Development

```powershell
# Pull latest changes
git pull origin main

# Make changes...

# Commit and push
git add .
git commit -m "Your changes"
git push origin main
```

### Release Workflow

```powershell
# 1. Update version (if needed)
# Edit package.json version

# 2. Build
npm run build:exe

# 3. Copy to releases
Copy-Item "dist\Auto_Punch IDE Setup 1.0.0.exe" "releases\"

# 4. Commit
git add .
git commit -m "Release v1.0.1"

# 5. Push
git push origin main

# 6. Create GitHub Release (optional)
# Go to: https://github.com/YOUR_USERNAME/Auto-Punch-IDE/releases/new
# Upload the EXE from releases folder
```

## File Organization

### Tracked Files
- ✅ All source code
- ✅ Configuration files
- ✅ Documentation
- ✅ `releases/` folder (EXE files)

### Ignored Files (in .gitignore)
- ❌ `dist/` - Build output
- ❌ `node_modules/` - Dependencies
- ❌ `__pycache__/` - Python cache
- ❌ `.env` - Environment variables
- ❌ Build artifacts

## Branch Strategy (Optional)

```powershell
# Create feature branch
git checkout -b feature/new-feature

# Make changes
# ...

# Commit
git add .
git commit -m "Add new feature"

# Push branch
git push origin feature/new-feature

# Merge to main (via GitHub or locally)
git checkout main
git merge feature/new-feature
git push origin main
```

## Telegram Integration (Separate Repo)

The Telegram integration is in a separate repository for:
- Independent deployment
- Separate versioning
- Easier maintenance
- Railway/Supabase configuration

### Setup Telegram Repo

1. Create separate private repo for Telegram integration
2. Copy Telegram-related files:
   - `telegram_bot.py`
   - `telegram_commands.py`
   - Railway config
   - Supabase config
3. Deploy to Railway
4. Configure webhooks

## Troubleshooting

### Authentication Issues
- Use Personal Access Token for HTTPS
- Or set up SSH keys
- Or use GitHub CLI: `gh auth login`

### Build Issues
- Ensure all dependencies installed
- Check Python and Node.js versions
- Clear `dist/` folder before rebuilding

### Push Issues
- Pull latest changes first: `git pull origin main`
- Resolve conflicts if any
- Then push: `git push origin main`

## Best Practices

1. ✅ Always pull before making changes
2. ✅ Test locally before pushing
3. ✅ Write clear commit messages
4. ✅ Keep releases folder updated
5. ✅ Document major changes
6. ✅ Use branches for major features
7. ✅ Keep Telegram integration separate

## Quick Reference

```powershell
# Status
git status

# Pull latest
git pull origin main

# Add all changes
git add .

# Commit
git commit -m "Message"

# Push
git push origin main

# Build
npm run build:exe

# Copy EXE to releases
Copy-Item "dist\Auto_Punch IDE Setup 1.0.0.exe" "releases\"
```

