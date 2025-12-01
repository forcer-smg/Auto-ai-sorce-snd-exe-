# 🧹 Cleanup Crashed/Installed Apps

## 🔍 Check What's Installed

Run this to see what's installed:
```powershell
.\cleanup-installed.ps1
```

This will show:
- ✅ Installed locations
- ✅ Running processes
- ✅ Uninstaller locations
- ✅ Cleanup options

## 🛑 Stop All Processes

**Option 1: PowerShell**
```powershell
.\force-close.ps1
```

**Option 2: Batch**
```cmd
.\force-cleanup.bat
```

## 🗑️ Remove Installed Apps

### Method 1: Use Uninstaller (Recommended)
If the script found an uninstaller, run it:
```powershell
Start-Process "C:\Program Files\Auto_Punch IDE\uninstall.exe"
```

### Method 2: Manual Deletion
After stopping all processes, manually delete:
- `C:\Program Files\Auto_Punch IDE`
- `C:\Program Files (x86)\Auto_Punch IDE`
- `%LOCALAPPDATA%\Programs\Auto_Punch IDE`
- `%APPDATA%\Auto_Punch IDE`

### Method 3: Reinstall Over (Easiest)
Just run the installer again - it will overwrite:
```powershell
.\run-installer.ps1
```

## ✅ After Cleanup

1. **Verify cleanup:**
   ```powershell
   .\cleanup-installed.ps1
   ```

2. **Reinstall fresh:**
   ```powershell
   .\run-installer.ps1
   ```

## 📋 Common Locations

- **Program Files:** `C:\Program Files\Auto_Punch IDE`
- **Program Files (x86):** `C:\Program Files (x86)\Auto_Punch IDE`
- **Local AppData:** `%LOCALAPPDATA%\Programs\Auto_Punch IDE`
- **AppData:** `%APPDATA%\Auto_Punch IDE`

## ⚠️ Important

1. **Stop all processes first** - Don't delete while app is running
2. **Use uninstaller if available** - Cleaner removal
3. **Check for leftovers** - Registry entries, shortcuts, etc.

## 🚀 Quick Cleanup

**Just run:**
```powershell
.\cleanup-installed.ps1
```

Then follow the instructions it shows!


