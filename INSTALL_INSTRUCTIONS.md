# 📦 Installation Instructions

## ✅ Quick Install

### Option 1: Automatic (Recommended)
```powershell
.\run-installer.ps1
```

This will:
1. ✅ Close any running Auto_Punch IDE instances
2. ✅ Run the installer automatically
3. ✅ Wait for installation to complete

### Option 2: Batch File
```cmd
.\close-and-install.bat
```

### Option 3: Manual Steps

1. **Close Auto_Punch IDE:**
   ```powershell
   .\force-close.ps1
   ```

2. **Run Installer:**
   - Double-click: `dist\Auto_Punch IDE Setup 1.0.0.exe`
   - Or run: `.\close-and-install.ps1`

## 🔧 If Installer Says "Cannot Close"

The installer needs to close the running application first. Use:

```powershell
.\force-close.ps1
```

Then run the installer again.

## 📋 Scripts Available

1. **run-installer.ps1** - Closes and installs (recommended)
2. **close-and-install.ps1** - PowerShell version
3. **close-and-install.bat** - Batch file version
4. **force-close.ps1** - Just closes processes

## ✅ After Installation

The installer will:
- Install Auto_Punch IDE to Program Files
- Create desktop shortcut
- Create Start Menu entry
- Make it available system-wide

## 🎯 Quick Command

**Just run this:**
```powershell
.\run-installer.ps1
```

It handles everything automatically!


