# Migration Guide: Web to Desktop App

## Overview

This guide helps you migrate from the web version to a professional Windows desktop application.

## Step-by-Step Migration

### Step 1: Backup ✅ DONE
- ✅ Backup created at: `C:\Users\Administrator\Auto_Punch IDE - BACKUP`
- This is your safety net - keep it!

### Step 2: Create New GitHub Repository

1. **Go to GitHub:**
   - Visit: https://github.com/new
   - Repository name: `Auto-Punch-IDE-Desktop`
   - Description: "Windows Desktop Application for Auto_Punch IDE"
   - Choose: Private or Public
   - **DO NOT** initialize with README (we have files)

2. **Push Current Code:**
   ```powershell
   cd "C:\Users\Administrator\Auto_Punch IDE"
   
   # Add new remote (if not exists)
   git remote add desktop https://github.com/SMG-Dawn/Auto-Punch-IDE-Desktop.git
   
   # Or if you want separate repo, create new one
   # Remove current remote first
   git remote remove origin
   git remote add origin https://github.com/SMG-Dawn/Auto-Punch-IDE-Desktop.git
   
   # Push to new repo
   git add .
   git commit -m "Initial desktop app setup"
   git push -u origin main
   ```

### Step 3: Install Dependencies

```powershell
# Install Node.js dependencies
npm install

# Install Python dependencies
pip install -r requirements.txt
```

### Step 4: Create Icons

1. Create or download icons:
   - Main icon: `resources/icon.ico` (256x256)
   - Installer icon: `resources/installer-icon.ico` (256x256)

2. Place in `resources/` folder

### Step 5: Test Development Build

```powershell
# Test in development mode
npm run dev
```

This should:
- Start Flask backend
- Open Electron window
- Show your IDE interface

### Step 6: Build Installers

```powershell
# Build both MSI and EXE
npm run build:all
```

Output will be in `dist/` folder:
- `Auto_Punch IDE Setup 1.0.0.msi`
- `Auto_Punch IDE Setup 1.0.0.exe`

### Step 7: Test Installation

1. Run the installer
2. Install to default location
3. Launch from Start Menu
4. Verify all features work

### Step 8: Set Up Auto-Updates

1. **Create GitHub Release:**
   - Go to GitHub repo → Releases
   - Click "Create a new release"
   - Tag: `v1.0.0`
   - Upload MSI and EXE installers
   - Publish release

2. **Test Update:**
   - Install version 1.0.0
   - Create version 1.0.1 release
   - App should detect and offer update

### Step 9: Integrate Telegram Bot

1. **Update Bot Code:**
   - Add commands from `TELEGRAM_INTEGRATION.md`
   - Deploy to Railway

2. **Set Up Webhook:**
   - GitHub → Settings → Webhooks
   - Add webhook URL from Railway
   - Select "Releases" event

3. **Test:**
   - Send `/desktop` command
   - Should return download links

## Repository Structure Decision

### Recommended: Separate Repos

**Current Setup:**
- `Auto-pounch-ai` (Web) → Railway deployment
- `Auto-Punch-IDE-Desktop` (Desktop) → GitHub Releases

**Benefits:**
- ✅ Clean separation
- ✅ Independent versioning
- ✅ No conflicts
- ✅ Easier maintenance

### Alternative: Monorepo

If you prefer one repo:
- Use branches: `web` and `desktop`
- Or folders: `web/` and `desktop/`
- More complex but unified

## Key Differences: Desktop vs Web

### Desktop App:
- ✅ Runs in Electron window (not browser)
- ✅ Starts Flask backend automatically
- ✅ No browser needed
- ✅ Better system integration
- ✅ Auto-updates via electron-updater
- ✅ Can run offline (except AI)

### Web Version:
- ✅ Runs in any browser
- ✅ Deployed to Railway
- ✅ Accessible from anywhere
- ✅ No installation needed
- ✅ Auto-deploys on git push

## Updating Both Versions

### Using Cursor IDE:

**Web Version:**
1. Edit code in Cursor
2. Commit and push to `Auto-pounch-ai` repo
3. Railway auto-deploys

**Desktop Version:**
1. Edit code in Cursor
2. Commit and push to `Auto-Punch-IDE-Desktop` repo
3. Build new installer: `npm run build:all`
4. Create GitHub release with new installers
5. Auto-updater notifies users

## Common Issues & Solutions

### Issue: Flask won't start
**Solution:** Check Python path in `electron/main.js`

### Issue: Port 5001 in use
**Solution:** Change port in `app.py` and `main.js`

### Issue: Build fails
**Solution:** 
```powershell
rm -r node_modules dist
npm install
npm run build
```

### Issue: Icons missing
**Solution:** Create icons and place in `resources/` folder

## Next Steps

1. ✅ Backup created
2. ⏳ Create GitHub repo
3. ⏳ Install dependencies
4. ⏳ Create icons
5. ⏳ Test development build
6. ⏳ Build installers
7. ⏳ Test installation
8. ⏳ Set up auto-updates
9. ⏳ Integrate Telegram bot
10. ⏳ Release first version

## Support

If you encounter issues:
1. Check `BUILD_INSTRUCTIONS.md`
2. Review error logs
3. Check GitHub Issues
4. Contact via Telegram bot


