# How to Place Background Image for Hacking Theme

## Quick Method (Drag & Drop)

1. **Locate your image file** (the Tai Lung image you want to use)
2. **Copy it** to this location:
   ```
   C:\Users\Administrator\Auto_Punch IDE\static\images\hacking-bg.jpg
   ```
3. **Or use PNG format:**
   ```
   C:\Users\Administrator\Auto_Punch IDE\static\images\hacking-bg.png
   ```

## Using the Batch Script

1. **Run the script:**
   - Double-click: `PLACE_BACKGROUND_IMAGE.bat`
   - Or run from terminal: `PLACE_BACKGROUND_IMAGE.bat`

2. **Enter the path** to your image file when prompted

3. **The script will automatically copy it** to the correct location

## Manual Method

### Option 1: Using File Explorer
1. Open File Explorer
2. Navigate to: `C:\Users\Administrator\Auto_Punch IDE\static\images\`
3. Copy your image file there
4. Rename it to: `hacking-bg.jpg` or `hacking-bg.png`

### Option 2: Using Command Line
```cmd
copy "C:\path\to\your\image.jpg" "C:\Users\Administrator\Auto_Punch IDE\static\images\hacking-bg.jpg"
```

## Supported Formats
- `.jpg` / `.jpeg`
- `.png`
- `.webp` (if you update the CSS)

## File Size Recommendations
- **Optimal**: 1920x1080 (Full HD)
- **Minimum**: 1280x720
- **Maximum file size**: 5MB (for best performance)

## After Placing the Image

1. **Restart the server** (if running)
2. **Hard refresh browser**: `Ctrl + Shift + R`
3. **Go to Settings** → **Appearance** → **Theme**
4. **Select "Hacking Mode (Cyberpunk)"**
5. **The background should appear!**

## Troubleshooting

**Image not showing?**
- Check file name is exactly: `hacking-bg.jpg` or `hacking-bg.png`
- Check file is in: `static\images\` folder
- Hard refresh browser (Ctrl+Shift+R)
- Check browser console (F12) for errors
- Verify file size isn't too large

**Image too dark/bright?**
- The CSS has an overlay - you can adjust it in `themes.css`
- Look for `rgba(10, 14, 39, 0.75)` and change the `0.75` value
- Lower = more transparent (image shows more)
- Higher = more opaque (darker overlay)

