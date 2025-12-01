# Manual EXE Upload to GitHub

## Quick Upload Guide

### Option 1: Via GitHub Web Interface (Easiest)

1. **Go to your repository:**
   ```
   https://github.com/YOUR_USERNAME/YOUR_REPO_NAME/releases/new
   ```

2. **Create a new release:**
   - Tag: `v1.0.0`
   - Title: `Auto_Punch IDE v1.0.0`
   - Description: Copy from `RELEASE_NOTES.md`

3. **Upload the executable:**
   - Drag and drop: `dist\Auto_Punch IDE Setup 1.0.0.exe`
   - Or click "Attach binaries" and select the file

4. **Publish release**

### Option 2: Using GitHub CLI (gh)

```powershell
# Install GitHub CLI if not installed
# Download from: https://cli.github.com/

# Authenticate
gh auth login

# Create release and upload
gh release create v1.0.0 `
  "dist\Auto_Punch IDE Setup 1.0.0.exe" `
  --title "Auto_Punch IDE v1.0.0" `
  --notes "$(Get-Content RELEASE_NOTES.md -Raw)"
```

### Option 3: Using PowerShell Script

```powershell
.\UPLOAD_EXE_TO_GITHUB.ps1
```

Follow the prompts to enter:
- Repository owner/username
- Repository name

The script will:
1. Clone the repository
2. Copy the executable
3. Commit and push

## File Location

The built executable is at:
```
dist\Auto_Punch IDE Setup 1.0.0.exe
```

Or if using unpacked version:
```
dist\win-unpacked\Auto_Punch IDE.exe
```

## Release Notes Template

See `RELEASE_NOTES.md` for complete release notes.

## Tips

- ✅ Use the installer (.exe) for releases
- ✅ Include release notes
- ✅ Tag with version number (v1.0.0)
- ✅ Mark as "Latest release" if it's the newest

