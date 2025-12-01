# Auto_Punch IDE - System Requirements

## Windows Desktop Application Requirements

### Minimum System Requirements

**Operating System:**
- Windows 10 (64-bit) or later
- Windows Server 2016 or later

**Hardware:**
- **Processor:** Intel Core i3 (2.0 GHz) or AMD equivalent
- **RAM:** 4 GB minimum (8 GB recommended)
- **Storage:** 500 MB free disk space for application
- **Display:** 1280x720 minimum resolution
- **Network:** Internet connection for updates and AI features

**Software Dependencies:**
- **Python 3.8+** (included in installer)
- **Node.js 18+** (included in installer)
- **Microsoft Visual C++ Redistributable 2015-2022** (included in installer)

### Recommended System Requirements

**Hardware:**
- **Processor:** Intel Core i5 (3.0 GHz) or AMD Ryzen 5 equivalent
- **RAM:** 16 GB or more
- **Storage:** 2 GB free disk space (for workspace and extensions)
- **Display:** 1920x1080 or higher
- **GPU:** Dedicated graphics card (optional, for better performance)

**Network:**
- Broadband internet connection (for AI features, updates, and cloud sync)
- Port 5001 available (default IDE port)

### Additional Requirements for Full Functionality

**For RedTeam Toolkit:**
- **Nmap:** Optional - for network scanning
- **Burp Suite Community Edition:** Optional - for web security testing
- **Java Runtime Environment (JRE) 11+:** Required if using Burp Suite

**For Git Integration:**
- **Git 2.30+:** Optional - for version control features

**For SSH Connections:**
- **OpenSSH Client:** Usually pre-installed on Windows 10+

**For Python Development:**
- **Python 3.8+:** For running Python scripts
- **pip:** Python package manager

**For JavaScript/Node.js Development:**
- **Node.js 18+:** For running JavaScript/TypeScript projects

### Installation Requirements

**Administrator Privileges:**
- Required for initial installation
- Required for installing system-level dependencies
- Not required for daily use

**Firewall/Antivirus:**
- May need to allow application through firewall
- Port 5001 should be allowed for local connections

### Browser Requirements (for Web Version)

If using the web version instead of desktop app:
- **Chrome 90+**, **Edge 90+**, **Firefox 88+**, or **Opera 76+**
- JavaScript enabled
- WebSocket support enabled

### Network Requirements

**Local Network:**
- Application runs on localhost:5001 by default
- No external network required for basic functionality

**Internet Connection:**
- Required for:
  - AI Assistant features
  - Extension marketplace
  - Auto-updates
  - Cloud workspace sync (if enabled)
  - GitHub integration

### Disk Space Breakdown

- **Application:** ~200 MB
- **Dependencies:** ~300 MB
- **Workspace:** Variable (depends on projects)
- **Extensions:** ~50-100 MB per extension
- **Cache/Temp:** ~100-500 MB

### Performance Notes

- Application uses Electron framework (Chromium-based)
- Memory usage: ~200-500 MB base + workspace size
- CPU usage: Low when idle, moderate during AI operations
- Startup time: 3-5 seconds on SSD, 5-10 seconds on HDD

### Compatibility

**Tested On:**
- Windows 10 (all versions)
- Windows 11 (all versions)
- Windows Server 2019/2022

**Not Supported:**
- Windows 7/8/8.1 (end of life)
- 32-bit Windows systems
- ARM-based Windows (Surface Pro X) - coming soon

### Troubleshooting Requirements

**If issues occur, ensure:**
1. Windows is up to date
2. All Windows updates installed
3. Antivirus not blocking application
4. Firewall allows localhost connections
5. Sufficient disk space available
6. No other application using port 5001

### Development Requirements (for building from source)

**For Building Desktop App:**
- Node.js 18+
- npm or yarn
- Python 3.8+
- Git
- Visual Studio Build Tools (for native modules)

**For Building Installer:**
- WiX Toolset 3.11+ (for MSI)
- Inno Setup 6+ (for EXE installer)
- Code signing certificate (optional, for distribution)


