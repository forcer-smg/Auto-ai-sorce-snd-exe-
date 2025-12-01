# Quick Install and Rebuild Guide

## One-Command Install and Rebuild

Run this single command to:
1. Add tools to RedTeam-Tools
2. Install all dependencies
3. Rebuild the app

```powershell
.\INSTALL_AND_REBUILD.ps1
```

## What It Does

### Step 1: Add Tools
- Clones 365-Stealer to `RedTeam-Tools/365-Stealer`
- Clones requests-ip-rotator to `RedTeam-Tools/requests-ip-rotator`

### Step 2: Install 365-Stealer Dependencies
- Installs Python packages from `requirements.txt`

### Step 3: Install requests-ip-rotator Dependencies
- Installs Python packages (from requirements.txt or as package)

### Step 4: Install Main App Dependencies
- Installs Flask, Supabase, and other app dependencies

### Step 5: Rebuild App
- Closes running processes
- Builds Electron app with all tools included

## Manual Steps (if script fails)

### 1. Add Tools
```powershell
cd "C:\Users\Administrator\Auto_Punch IDE\RedTeam-Tools"
git clone https://github.com/AlteredSecurity/365-Stealer.git
git clone https://github.com/Ge0rg3/requests-ip-rotator.git
```

### 2. Install Dependencies
```powershell
cd "C:\Users\Administrator\Auto_Punch IDE"

# 365-Stealer
cd RedTeam-Tools\365-Stealer
pip install -r requirements.txt
cd ..\..

# requests-ip-rotator
cd RedTeam-Tools\requests-ip-rotator
pip install -r requirements.txt
cd ..\..

# Main app
pip install -r requirements.txt
```

### 3. Rebuild
```powershell
.\CLEAN_REBUILD.ps1
```

## Expected Output

```
============================================================
  INSTALLING DEPENDENCIES AND REBUILDING
============================================================

[1/5] Adding tools to RedTeam-Tools...
  [+] 365-Stealer added
  [+] requests-ip-rotator added

[2/5] Installing 365-Stealer dependencies...
  [+] 365-Stealer dependencies installed

[3/5] Installing requests-ip-rotator dependencies...
  [+] requests-ip-rotator dependencies installed

[4/5] Installing main app dependencies...
  [+] Main app dependencies installed

[5/5] Rebuilding application...
  ...
  BUILD SUCCESSFUL!
```

## After Rebuild

Test the build:
```powershell
.\TEST_BUILD.ps1
```

The new tools will be available in:
- Toolkit Panel in the IDE
- AI Chat (ask Auto_Punch Ai to use them)
- Terminal (execute directly)

