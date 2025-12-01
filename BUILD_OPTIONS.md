# 🔧 Alternative Build Methods

If the main build script isn't working, try these alternatives:

## Method 1: Simple Batch File (Easiest)

```cmd
.\build-simple.bat
```

**Pros:**
- No PowerShell issues
- Simple and straightforward
- Works in CMD

## Method 2: Direct PowerShell

```powershell
.\build-direct.ps1
```

**Pros:**
- Minimal script
- No complex logic
- Just runs the build

## Method 3: Manual Commands

**Step 1: Open PowerShell or CMD**
```powershell
cd "C:\Users\Administrator\Auto_Punch IDE"
```

**Step 2: Refresh PATH (if needed)**
```powershell
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
```

**Step 3: Build**
```powershell
npm run build:exe
```

**Step 4: Check result**
```powershell
dir dist\*.exe
```

## Method 4: Using CMD Only

```cmd
cd "C:\Users\Administrator\Auto_Punch IDE"
npm run build:exe
```

## Method 5: Node.js Direct

If npm scripts don't work:

```powershell
npx electron-builder --win --x64 --config.win.target=nsis
```

## Method 6: Clean Build

If previous builds caused issues:

```powershell
# Clean everything
Remove-Item -Path "dist" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "node_modules\.cache" -Recurse -Force -ErrorAction SilentlyContinue

# Rebuild
npm run build:exe
```

## Method 7: Step-by-Step Manual

1. **Clean:**
   ```powershell
   Remove-Item dist -Recurse -Force
   ```

2. **Verify Node:**
   ```powershell
   node --version
   npm --version
   ```

3. **Install dependencies (if needed):**
   ```powershell
   npm install
   ```

4. **Build:**
   ```powershell
   npm run build:exe
   ```

5. **Check output:**
   ```powershell
   Test-Path "dist\Auto_Punch IDE Setup 1.0.0.exe"
   ```

## 🐛 Troubleshooting

### If npm run build:exe fails:

**Try:**
```powershell
npm run build:exe -- --force
```

### If electron-builder fails:

**Try:**
```powershell
npx electron-builder --win --x64 --config.win.target=nsis --config.directories.output=dist
```

### If PATH issues:

**Use full path:**
```powershell
& "C:\Program Files\nodejs\npm.cmd" run build:exe
```

### If still not working:

**Check package.json scripts:**
```powershell
Get-Content package.json | Select-String "build:exe"
```

Should show:
```json
"build:exe": "electron-builder --win --x64 --config.win.target=nsis"
```

## ✅ Recommended Order

1. **Try:** `.\build-simple.bat` (easiest)
2. **Try:** `.\build-direct.ps1` (simple PowerShell)
3. **Try:** Manual commands (full control)
4. **Try:** Clean build (if issues persist)

## 📋 Quick Reference

**Simplest:**
```cmd
build-simple.bat
```

**Direct:**
```powershell
npm run build:exe
```

**Full path:**
```powershell
& "C:\Program Files\nodejs\npm.cmd" run build:exe
```

## 🎯 Success Indicators

After build, you should see:
- `dist\Auto_Punch IDE Setup 1.0.0.exe` (installer)
- `dist\win-unpacked\Auto_Punch IDE.exe` (portable)

If these exist, build was successful!


