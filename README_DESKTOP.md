# Auto_Punch IDE - Desktop Application

## 🚀 Quick Start

### For End Users

1. **Download:**
   - Download `Auto_Punch IDE Setup.exe` (recommended) or `.msi` file
   - Run the installer
   - Follow installation wizard

2. **Launch:**
   - Find "Auto_Punch IDE" in Start Menu
   - Or double-click desktop shortcut
   - App opens in its own window (no browser needed!)

3. **First Run:**
   - App starts Flask backend automatically
   - Window opens when ready (3-5 seconds)
   - All features work offline (except AI features)

### For Developers

See [BUILD_INSTRUCTIONS.md](BUILD_INSTRUCTIONS.md) for building from source.

## 📋 System Requirements

See [SYSTEM_REQUIREMENTS.md](SYSTEM_REQUIREMENTS.md) for complete requirements.

**Minimum:**
- Windows 10 (64-bit)
- 4 GB RAM
- 500 MB disk space

## 🔄 Auto-Updates

The app checks for updates:
- On startup
- Manually via Help → Check for Updates

Updates download automatically and install on restart.

## 🆚 Desktop vs Web Version

| Feature | Desktop | Web |
|---------|---------|-----|
| Runs in browser | ❌ | ✅ |
| Runs standalone | ✅ | ❌ |
| Auto-updates | ✅ | ✅ (Railway) |
| Offline mode | ✅ | ❌ |
| System integration | ✅ | ❌ |
| File associations | ✅ | ❌ |
| Better performance | ✅ | ⚠️ |

## 🛠️ Troubleshooting

### App Won't Start
1. Check Windows Event Viewer for errors
2. Ensure port 5001 is not in use
3. Run as administrator (if needed)
4. Check antivirus isn't blocking

### Updates Not Working
1. Check internet connection
2. Verify GitHub Releases accessible
3. Check firewall settings
4. Try manual update check

### Backend Not Starting
1. Check Python is installed
2. Verify all dependencies installed
3. Check app logs in `%APPDATA%/Auto_Punch IDE/logs/`

## 📞 Support

- **GitHub Issues:** [Create Issue](https://github.com/SMG-Dawn/Auto-Punch-IDE-Desktop/issues)
- **Telegram Bot:** `/help` command
- **Documentation:** See docs folder

## 🔐 Security

- App runs locally (no cloud data)
- All code execution is local
- AI features require internet
- No telemetry or tracking

## 📝 License

Proprietary - Auto_Punch Ai © 2025


