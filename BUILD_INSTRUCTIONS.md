# Auto_Punch IDE - Build Instructions

## Prerequisites

### Required Software
1. **Node.js 18+** - [Download](https://nodejs.org/)
2. **Python 3.8+** - [Download](https://www.python.org/)
3. **Git** - [Download](https://git-scm.com/)
4. **Visual Studio Build Tools** (for native modules) - [Download](https://visualstudio.microsoft.com/downloads/)

### Install Prerequisites
```powershell
# Check Node.js
node --version

# Check Python
python --version

# Check Git
git --version
```

## Initial Setup

### 1. Install Node.js Dependencies
```powershell
cd "C:\Users\Administrator\Auto_Punch IDE"
npm install
```

### 2. Install Python Dependencies
```powershell
pip install -r requirements.txt
```

### 3. Development Mode
```powershell
# Run in development (opens browser)
npm run dev

# Or run with Flask auto-start
npm run start
```

## Building the Desktop Application

### Build for Windows (Both MSI and EXE)
```powershell
npm run build:all
```

### Build MSI Only
```powershell
npm run build:msi
```

### Build EXE Only
```powershell
npm run build:exe
```

### Build Output
- **MSI Installer:** `dist/Auto_Punch IDE Setup 1.0.0.msi`
- **EXE Installer:** `dist/Auto_Punch IDE Setup 1.0.0.exe`
- **Portable:** `dist/win-unpacked/Auto_Punch IDE.exe`

## Creating Icons

### Required Icon Files
1. `resources/icon.ico` - Main application icon (256x256)
2. `resources/installer-icon.ico` - Installer icon (256x256)

### Create Icons
Use an online converter or tool like:
- [ICO Convert](https://icoconvert.com/)
- [ConvertICO](https://convertico.com/)

Place converted `.ico` files in the `resources/` directory.

## Testing the Build

### Test Portable Version
```powershell
cd dist\win-unpacked
.\Auto_Punch IDE.exe
```

### Test Installer
1. Run the MSI or EXE installer
2. Install to default location
3. Launch from Start Menu or Desktop shortcut
4. Verify all features work

## Distribution

### GitHub Releases
1. Create a new release on GitHub
2. Upload both MSI and EXE installers
3. Tag with version number (e.g., `v1.0.0`)
4. Auto-updater will detect new releases

### Manual Distribution
- Upload installers to file hosting
- Share download links via Telegram bot
- Include in website downloads

## Troubleshooting

### Build Fails
```powershell
# Clean and rebuild
rm -r node_modules
rm -r dist
npm install
npm run build
```

### Python Not Found
- Ensure Python is in PATH
- Or specify full path in `main.js`

### Port Already in Use
- Change port in `app.py` and `main.js`
- Or close other applications using port 5001

### Missing Dependencies
```powershell
# Reinstall all dependencies
npm install
pip install -r requirements.txt --upgrade
```

## Advanced Configuration

### Custom Installer Settings
Edit `package.json` → `build` section:
- Change app name
- Modify installer behavior
- Add custom installation steps

### Code Signing (Optional)
1. Obtain code signing certificate
2. Add to `package.json`:
```json
"win": {
  "certificateFile": "path/to/certificate.pfx",
  "certificatePassword": "password"
}
```

## CI/CD Setup (GitHub Actions)

Create `.github/workflows/build.yml`:
```yaml
name: Build Desktop App

on:
  push:
    tags:
      - 'v*'

jobs:
  build:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - uses: actions/setup-python@v4
        with:
          python-version: '3.8'
      - run: npm install
      - run: pip install -r requirements.txt
      - run: npm run build:all
      - uses: actions/upload-artifact@v3
        with:
          name: installers
          path: dist/*.exe
```


