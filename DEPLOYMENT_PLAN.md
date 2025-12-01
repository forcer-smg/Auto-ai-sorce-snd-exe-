# Auto_Punch IDE - Deployment & Repository Plan

## Repository Structure Strategy

### Recommended: Separate Repositories

**Repository 1: `Auto-Punch-IDE-Web`** (Current)
- Web-based version
- Flask backend
- Browser-based interface
- Deployed to Railway/Supabase
- Telegram bot integration (current)

**Repository 2: `Auto-Punch-IDE-Desktop`** (New)
- Windows desktop application
- Electron wrapper
- Standalone executable
- Auto-update mechanism
- Same Flask backend, different frontend delivery

### Benefits of Separate Repos:
1. ✅ Clean separation of concerns
2. ✅ Independent versioning
3. ✅ Different deployment pipelines
4. ✅ Easier maintenance
5. ✅ No conflicts between web and desktop features
6. ✅ Can share common code via submodules or packages

## Implementation Plan

### Phase 1: Setup & Structure

1. **Create New GitHub Repository**
   - Name: `Auto-Punch-IDE-Desktop`
   - Description: "Windows Desktop Application for Auto_Punch IDE"
   - Private or Public (your choice)

2. **Repository Structure**
   ```
   Auto-Punch-IDE-Desktop/
   ├── app/                    # Flask backend (shared)
   ├── electron/               # Electron main process
   ├── build/                  # Build scripts
   ├── dist/                   # Built executables
   ├── installer/              # Installer configs
   ├── resources/              # Icons, assets
   ├── package.json           # Node.js dependencies
   ├── requirements.txt       # Python dependencies
   ├── main.js                # Electron entry point
   ├── preload.js             # Electron preload script
   └── README.md
   ```

### Phase 2: Electron Integration

**Technology Stack:**
- **Electron 28+** - Desktop framework
- **electron-builder** - Packaging & installer creation
- **electron-updater** - Auto-update mechanism
- **Flask** - Backend API (embedded)
- **Python** - Backend runtime

**Architecture:**
```
┌─────────────────────────────────────┐
│     Electron Main Process           │
│  (Node.js - main.js)                │
│  - Window management                │
│  - Auto-update                      │
│  - System integration               │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│     Electron Renderer Process       │
│  (Chromium - UI)                    │
│  - Monaco Editor                    │
│  - React/Vanilla JS UI              │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│     Flask Backend (Python)          │
│  - API endpoints                    │
│  - Socket.IO                        │
│  - File operations                  │
│  - AI integration                   │
└─────────────────────────────────────┘
```

### Phase 3: Build System

**MSI vs EXE Installer:**

**MSI (Recommended for Enterprise):**
- ✅ Windows standard
- ✅ Better for corporate deployment
- ✅ Group Policy support
- ✅ Silent installation
- ✅ Professional appearance
- ❌ More complex to create

**EXE (Recommended for End Users):**
- ✅ Simpler for users
- ✅ Easier to create
- ✅ Custom installation wizard
- ✅ Better for personal use
- ❌ Less enterprise-friendly

**Recommendation: Provide BOTH**
- MSI for enterprise/corporate users
- EXE for individual users
- Both created from same build process

### Phase 4: Auto-Update Mechanism

**Update Strategy:**
1. **Check on Startup:** Check for updates when app launches
2. **Background Check:** Periodic checks (daily)
3. **Manual Check:** User can check from Help menu
4. **Update Server:** GitHub Releases or custom server
5. **Delta Updates:** Only download changed files
6. **Rollback:** Keep previous version for rollback

**Implementation:**
- Use `electron-updater` package
- Host updates on GitHub Releases
- Version checking via API
- Download and install updates automatically
- Show progress to user

### Phase 5: Telegram Integration

**Current Setup:**
- Telegram bot connected to GitHub repo
- Auto-push to Railway on edits
- Supabase integration active

**Integration Plan:**
1. **Keep Web Version:** Current Telegram bot continues working
2. **Add Desktop Notifications:** Desktop app can receive Telegram notifications
3. **Sync Settings:** Share settings between web and desktop via Supabase
4. **Update Notifications:** Telegram bot can notify about desktop app updates
5. **Remote Control:** Telegram bot can trigger actions in desktop app (optional)

**Telegram Bot Enhancements:**
- `/desktop-status` - Check desktop app status
- `/desktop-update` - Trigger desktop app update
- `/sync-settings` - Sync settings between web and desktop

### Phase 6: Development Workflow

**Using Cursor IDE:**
1. **Web Version:** Edit in Cursor → Push to GitHub → Auto-deploy to Railway
2. **Desktop Version:** Edit in Cursor → Push to Desktop repo → Build locally or CI/CD
3. **Shared Code:** Use git submodules or npm packages for shared components

**Update Process:**
1. Make changes in Cursor
2. Test locally
3. Commit and push to respective repo
4. Web: Auto-deploys via Railway
5. Desktop: Build new installer → Upload to GitHub Releases → Auto-update triggers

## File Structure Details

### Desktop App Structure

```
Auto-Punch-IDE-Desktop/
├── app/                          # Flask backend
│   ├── app.py
│   ├── security_toolkit.py
│   ├── agent_workflow.py
│   └── ...
├── electron/
│   ├── main.js                   # Electron main process
│   ├── preload.js                # Preload script
│   └── updater.js                # Update logic
├── build/
│   ├── build.js                  # Build script
│   ├── package.js                # Package script
│   └── installer.js              # Installer creation
├── resources/
│   ├── icon.ico                  # App icon
│   ├── installer-icon.ico         # Installer icon
│   └── splash.png                # Splash screen
├── dist/                         # Output directory
│   ├── win-unpacked/             # Unpacked app
│   ├── *.exe                     # Portable executable
│   └── installers/               # Installers
│       ├── Auto_Punch_IDE.msi    # MSI installer
│       └── Auto_Punch_IDE.exe    # EXE installer
├── package.json                  # Node.js config
├── requirements.txt              # Python dependencies
├── electron-builder.yml          # Build configuration
├── .github/
│   └── workflows/
│       └── build.yml             # CI/CD for building
└── README.md
```

## Build Commands

```bash
# Install dependencies
npm install
pip install -r requirements.txt

# Development
npm run dev                    # Run Electron in dev mode
npm run start                  # Start Flask backend

# Build
npm run build                  # Build Electron app
npm run build:win              # Build for Windows
npm run build:msi              # Create MSI installer
npm run build:exe              # Create EXE installer
npm run build:all              # Build both installers

# Package
npm run package                # Package without installer
npm run dist                   # Create distributables
```

## Update Mechanism

### Version Management
- Semantic versioning: `MAJOR.MINOR.PATCH`
- Example: `1.0.0`, `1.0.1`, `1.1.0`
- Stored in `package.json` and `app/__version__.py`

### Update Flow
1. Developer releases new version on GitHub
2. Desktop app checks for updates (on startup or manually)
3. If update available, download automatically
4. Show update notification to user
5. User approves → Install in background
6. Restart app with new version

### Update Server Options
- **Option 1:** GitHub Releases (free, easy)
- **Option 2:** Custom server (more control)
- **Option 3:** Supabase storage (already integrated)

## Testing Strategy

1. **Local Testing:** Test in development mode
2. **Build Testing:** Test built executable locally
3. **Installer Testing:** Test MSI and EXE installers
4. **Update Testing:** Test auto-update mechanism
5. **Cross-Version Testing:** Test updates from old to new versions

## Distribution

### Distribution Channels
1. **GitHub Releases:** Primary distribution
2. **Website Download:** Direct download link
3. **Telegram Bot:** `/download` command
4. **Auto-Update:** Built-in update mechanism

### Code Signing (Optional but Recommended)
- Sign executables with code signing certificate
- Prevents Windows security warnings
- Professional appearance
- Required for Windows Store (if applicable)

## Backup Strategy

✅ **Current Backup Created:**
- Location: `C:\Users\Administrator\Auto_Punch IDE - BACKUP`
- Contains: Complete working copy
- Purpose: Rollback if needed

**Additional Backups:**
- Git repository (version control)
- GitHub remote (cloud backup)
- Local backup (current)

## Next Steps

1. ✅ Backup created
2. ⏳ Create new GitHub repository
3. ⏳ Set up Electron structure
4. ⏳ Integrate Flask backend
5. ⏳ Create build system
6. ⏳ Implement auto-update
7. ⏳ Test installation process
8. ⏳ Integrate with Telegram bot
9. ⏳ Create documentation
10. ⏳ Release first version


