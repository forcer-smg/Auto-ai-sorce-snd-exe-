# Icons Required for Desktop App

## Required Icon Files

Place these icon files in the `resources/` directory:

1. **icon.ico** (256x256)
   - Main application icon
   - Used in taskbar, window title, etc.
   - Format: ICO (Windows icon format)

2. **installer-icon.ico** (256x256)
   - Installer icon
   - Used in MSI and EXE installers
   - Format: ICO (Windows icon format)

## Creating Icons

### Option 1: Online Converter
1. Create or find a 256x256 PNG image
2. Use online converter:
   - https://icoconvert.com/
   - https://convertico.com/
   - https://www.icoconverter.com/
3. Download as `.ico` file
4. Save to `resources/` folder

### Option 2: Using Image Editor
1. Create 256x256 image in Photoshop/GIMP/etc.
2. Export as PNG
3. Convert to ICO using converter
4. Save to `resources/` folder

### Option 3: Use Default (Temporary)
- electron-builder will use default Electron icon if missing
- You can add custom icons later
- App will still build and work

## Icon Design Tips

- **Size:** 256x256 pixels minimum
- **Format:** ICO (Windows icon format)
- **Style:** Professional, recognizable
- **Colors:** Works in light and dark themes
- **Simple:** Clear at small sizes (16x16, 32x32)

## Quick Test

After adding icons, verify:
```powershell
Test-Path "resources\icon.ico"
Test-Path "resources\installer-icon.ico"
```

Both should return `True`.

## Note

Icons are optional for initial build - electron-builder will use defaults.
You can add custom icons anytime before final release.


