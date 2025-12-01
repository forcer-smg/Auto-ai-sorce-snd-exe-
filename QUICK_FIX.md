# Quick Fix: Build Error "Access is denied"

## Problem
The build fails because the Auto_Punch IDE executable is still running from a previous test.

## Solution

### Option 1: Use the Clean Rebuild Script (Easiest)
```powershell
.\CLEAN_REBUILD.ps1
```

This script will:
1. Close all Auto_Punch IDE processes
2. Close Python Flask processes
3. Wait for cleanup
4. Rebuild the app

### Option 2: Manual Steps

1. **Close the Auto_Punch IDE window** if it's open
2. **Close any Python/Flask processes**:
   ```powershell
   Get-Process python | Stop-Process -Force
   ```
3. **Wait a few seconds**, then rebuild:
   ```powershell
   npm run build:exe
   ```

### Option 3: Task Manager
1. Press `Ctrl+Shift+Esc` to open Task Manager
2. Find and end:
   - "Auto_Punch IDE.exe"
   - "electron" processes
   - "python.exe" processes running app.py
3. Then rebuild:
   ```powershell
   npm run build:exe
   ```

## Why This Happens
When you test the built executable, it locks the file. The build process needs exclusive access to replace it, so you must close the running app first.

## Prevention
Always close the app before rebuilding, or use the `CLEAN_REBUILD.ps1` script which handles this automatically.

