const { app, BrowserWindow, Menu, ipcMain, dialog, shell } = require('electron');
const path = require('path');
const { spawn, execSync } = require('child_process');
const fs = require('fs');

// Try to load electron-updater, but make it optional
let autoUpdater = null;
try {
  autoUpdater = require('electron-updater').autoUpdater;
} catch (error) {
  console.warn('electron-updater not available:', error.message);
  // Create a dummy autoUpdater object
  autoUpdater = {
    checkForUpdatesAndNotify: () => {},
    checkForUpdates: () => {},
    on: () => {},
    quitAndInstall: () => {}
  };
}

// Keep a global reference of the window object
let mainWindow;
let flaskProcess = null;
const isDev = process.env.NODE_ENV === 'development' || !app.isPackaged;

// Flask server configuration
// Load config for server URL (local or remote)
let serverConfig = { serverUrl: `http://localhost:5001`, useLocalServer: true };
try {
  serverConfig = require('./config.json');
} catch (e) {
  console.log('Using default local server configuration');
}

const FLASK_PORT = 5001;
const FLASK_URL = serverConfig.useLocalServer 
  ? `http://localhost:${FLASK_PORT}`
  : (serverConfig.serverUrl || serverConfig.railwayUrl || `http://localhost:${FLASK_PORT}`);

// Enable auto-updater in production (if available)
if (!isDev && autoUpdater && autoUpdater.checkForUpdatesAndNotify) {
  try {
    autoUpdater.checkForUpdatesAndNotify();
    
    autoUpdater.on('update-available', () => {
      if (mainWindow) {
        dialog.showMessageBox(mainWindow, {
          type: 'info',
          title: 'Update Available',
          message: 'A new version is available. It will be downloaded in the background.',
          buttons: ['OK']
        });
      }
    });

    autoUpdater.on('update-downloaded', () => {
      if (mainWindow) {
        dialog.showMessageBox(mainWindow, {
          type: 'info',
          title: 'Update Ready',
          message: 'Update downloaded. The application will restart to apply the update.',
          buttons: ['Restart Now', 'Later']
        }).then((result) => {
          if (result.response === 0) {
            autoUpdater.quitAndInstall();
          }
        });
      }
    });
  } catch (error) {
    console.warn('Auto-updater initialization failed:', error.message);
  }
}

function createWindow() {
  // Create the browser window
  mainWindow = new BrowserWindow({
    width: 1400,
    height: 900,
    minWidth: 800,
    minHeight: 600,
    icon: path.join(__dirname, '../resources/icon.ico'),
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js'),
      webSecurity: true
    },
    show: false, // Don't show until ready
    titleBarStyle: 'default',
    frame: true
  });

  // Show window when ready to prevent visual flash
  mainWindow.once('ready-to-show', () => {
    mainWindow.show();
    
    // Focus the window
    if (isDev) {
      mainWindow.webContents.openDevTools();
    }
  });

  // Load the Flask app
  const startUrl = FLASK_URL;
  
  // Wait for Flask to be ready, then load
  // Give Flask extra time to initialize (it loads Auto_Punch Ai components)
  waitForServer(startUrl, () => {
    console.log('Loading Flask app in window...');
    mainWindow.loadURL(startUrl);
  }, 90); // Increased to 90 seconds to allow Auto_Punch Ai initialization
  
  // Fallback: If detection fails but server is running, try loading after 10 seconds
  setTimeout(() => {
    if (mainWindow && !mainWindow.webContents.getURL()) {
      console.log('Fallback: Attempting to load Flask app...');
      mainWindow.loadURL(startUrl).catch(err => {
        console.error('Failed to load Flask app:', err);
      });
    }
  }, 10000); // Try after 10 seconds as fallback

  // Handle window closed
  mainWindow.on('closed', () => {
    mainWindow = null;
  });

  // Handle external links
  mainWindow.webContents.setWindowOpenHandler(({ url }) => {
    shell.openExternal(url);
    return { action: 'deny' };
  });

  // Create application menu
  createMenu();
}

function waitForServer(url, callback, maxAttempts = 60) {
  const http = require('http');
  const urlObj = new URL(url);
  const hostname = urlObj.hostname;
  const port = urlObj.port || (urlObj.protocol === 'https:' ? 443 : 80);
  let attemptCount = 0;
  
  const attempt = () => {
    attemptCount++;
    // Only log every 5 attempts to reduce spam
    if (attemptCount % 5 === 0 || attemptCount <= 5) {
      console.log(`Waiting for Flask server... (attempt ${attemptCount}/${maxAttempts})`);
    }
    
    if (attemptCount >= maxAttempts) {
      console.error('Flask server detection timeout after', maxAttempts, 'attempts');
      // Try one final check - server might be running but detection failed
      console.log('Performing final server check...');
      const finalCheck = http.get({
        hostname: hostname,
        port: port,
        path: '/',
        timeout: 3000
      }, (res) => {
        console.log('Final check: Server responded with status', res.statusCode);
        // Any response means server is running
        callback();
      });
      
      finalCheck.on('error', (err) => {
        console.error('Final check failed:', err.message);
        // Still try to load - server might be running
        console.log('Attempting to load anyway - server may be running...');
        callback();
      });
      
      finalCheck.setTimeout(3000, () => {
        finalCheck.destroy();
        console.log('Final check timeout - attempting to load anyway...');
        callback();
      });
      return;
    }

    const req = http.get({
      hostname: hostname,
      port: port,
      path: '/',
      timeout: 2000
    }, (res) => {
      // Any status code means server is running (even 500 is OK - server is up)
      console.log('Flask server is ready! Status:', res.statusCode);
      callback();
    });

    req.on('error', (err) => {
      // Connection refused means server not ready yet - keep trying
      if (err.code === 'ECONNREFUSED') {
        setTimeout(attempt, 1000);
      } else if (err.code === 'ETIMEDOUT') {
        // Timeout might mean server is slow - try again
        setTimeout(attempt, 1000);
      } else {
        // Other errors - log but keep trying
        if (attemptCount % 10 === 0) {
          console.log('Connection error (will retry):', err.code);
        }
        setTimeout(attempt, 1000);
      }
    });

    req.setTimeout(2000, () => {
      req.destroy();
      setTimeout(attempt, 1000);
    });
  };

  // Start checking after a short delay to give Flask time to start
  setTimeout(attempt, 2000);
}

function startFlaskServer() {
  if (flaskProcess) {
    return; // Already running
  }

  // Find app.py - try multiple locations
  let appPath = null;
  if (isDev) {
    appPath = path.join(__dirname, '..', 'app.py');
  } else {
    // In packaged app, files are unpacked from ASAR
    // Try different possible locations in packaged app
    const possiblePaths = [
      path.join(process.resourcesPath, 'app.asar.unpacked', 'app.py'),
      path.join(process.resourcesPath, 'app.py'),
      path.join(process.resourcesPath, 'app', 'app.py'),
      path.join(app.getAppPath(), 'app.py'),
      path.join(__dirname, '..', 'app.py'),
      path.join(process.resourcesPath, '..', 'app.asar.unpacked', 'app.py')
    ];
    
    for (const possiblePath of possiblePaths) {
      if (fs.existsSync(possiblePath)) {
        appPath = possiblePath;
        break;
      }
    }
  }

  if (!appPath || !fs.existsSync(appPath)) {
    console.error('Flask app.py not found!');
    console.error('Searched paths:', isDev ? [appPath] : [
      path.join(process.resourcesPath, 'app.py'),
      path.join(process.resourcesPath, 'app', 'app.py'),
      path.join(app.getAppPath(), 'app.py')
    ]);
    dialog.showErrorBox(
      'Configuration Error',
      'Flask application file (app.py) not found. Please reinstall the application.'
    );
    app.quit();
    return;
  }

  // Find Python executable - try multiple methods (synchronously)
  let pythonExecutable = null;
  
  // Function to test if Python executable works
  function testPython(pyPath) {
    try {
      if (process.platform === 'win32') {
        // On Windows, use where command or direct test
        try {
          const result = execSync(`"${pyPath}" --version`, { 
            encoding: 'utf8', 
            timeout: 2000,
            stdio: 'pipe'
          });
          if (result && result.trim()) {
            return true;
          }
        } catch (e) {
          return false;
        }
      } else {
        // On Unix-like systems
        try {
          execSync(`"${pyPath}" --version`, { 
            encoding: 'utf8', 
            timeout: 2000,
            stdio: 'pipe'
          });
          return true;
        } catch (e) {
          return false;
        }
      }
    } catch (e) {
      return false;
    }
    return false;
  }

  // Try to find Python using 'where' command on Windows
  if (process.platform === 'win32') {
    try {
      const whereResult = execSync('where python', { 
        encoding: 'utf8', 
        timeout: 2000,
        stdio: 'pipe'
      });
      const pythonPath = whereResult.split('\n')[0].trim();
      if (pythonPath && testPython(pythonPath)) {
        pythonExecutable = pythonPath;
      }
    } catch (e) {
      // where command failed, try other methods
    }
    
    // Try 'py' launcher
    if (!pythonExecutable) {
      try {
        const pyResult = execSync('where py', { 
          encoding: 'utf8', 
          timeout: 2000,
          stdio: 'pipe'
        });
        const pyPath = pyResult.split('\n')[0].trim();
        if (pyPath && testPython(pyPath)) {
          pythonExecutable = pyPath;
        }
      } catch (e) {
        // py launcher not found
      }
    }
  }

  // Try common Python paths
  if (!pythonExecutable) {
    const pythonPaths = [
      'python',
      'python3',
      'py',
      'C:\\Python314\\python.exe',
      'C:\\Python313\\python.exe',
      'C:\\Python312\\python.exe',
      'C:\\Python311\\python.exe',
      'C:\\Python310\\python.exe',
      'C:\\Python39\\python.exe',
      'C:\\Python38\\python.exe',
      'C:\\Program Files\\Python314\\python.exe',
      'C:\\Program Files\\Python313\\python.exe',
      'C:\\Program Files\\Python312\\python.exe',
      'C:\\Program Files\\Python311\\python.exe',
      'C:\\Program Files (x86)\\Python314\\python.exe',
      'C:\\Program Files (x86)\\Python313\\python.exe',
      'C:\\Program Files (x86)\\Python312\\python.exe',
      'C:\\Program Files (x86)\\Python311\\python.exe',
      process.env.LOCALAPPDATA ? path.join(process.env.LOCALAPPDATA, 'Programs', 'Python', 'Python314', 'python.exe') : null,
      process.env.LOCALAPPDATA ? path.join(process.env.LOCALAPPDATA, 'Programs', 'Python', 'Python313', 'python.exe') : null,
      process.env.LOCALAPPDATA ? path.join(process.env.LOCALAPPDATA, 'Programs', 'Python', 'Python312', 'python.exe') : null,
      process.env.LOCALAPPDATA ? path.join(process.env.LOCALAPPDATA, 'Programs', 'Python', 'Python311', 'python.exe') : null,
      process.env.APPDATA ? path.join(process.env.APPDATA, '..', 'Local', 'Programs', 'Python', 'Python314', 'python.exe') : null,
      process.env.APPDATA ? path.join(process.env.APPDATA, '..', 'Local', 'Programs', 'Python', 'Python313', 'python.exe') : null,
    ].filter(p => p !== null);
    
    for (const pyPath of pythonPaths) {
      if (testPython(pyPath)) {
        pythonExecutable = pyPath;
        break;
      }
    }
  }

  // If still not found, default to 'python' and let spawn handle the error
  if (!pythonExecutable) {
    pythonExecutable = 'python';
  }

  // Verify Python was found before proceeding
  if (!pythonExecutable || pythonExecutable === 'python') {
    // Last attempt: test if 'python' works
    if (!testPython('python')) {
      dialog.showErrorBox(
        'Python Not Found',
        `Python is required to run the backend server.\n\n` +
        `Python was not found in your system PATH or common installation locations.\n\n` +
        `Please:\n` +
        `1. Install Python 3.11 or later from https://www.python.org/downloads/\n` +
        `2. During installation, check "Add Python to PATH"\n` +
        `3. Restart your computer after installation\n` +
        `4. Then restart Auto_Punch IDE\n\n` +
        `Alternatively, you can run the IDE in development mode using run.bat`
      );
      app.quit();
      return;
    }
  }

  console.log('Starting Flask server...');
  console.log('Python:', pythonExecutable);
  console.log('App:', appPath);
  
  // Determine working directory
  let workingDir;
  if (isDev) {
    workingDir = path.join(__dirname, '..');
  } else {
    // In production, use the unpacked resources directory
    // This ensures requirements.txt and other files are accessible
    const unpackedDir = path.join(process.resourcesPath, 'app.asar.unpacked');
    if (fs.existsSync(unpackedDir)) {
      workingDir = unpackedDir;
    } else {
      workingDir = path.dirname(appPath);
    }
  }
  
  console.log('Working directory:', workingDir);
  
  try {
    // Prepare spawn options
    const spawnOptions = {
      cwd: workingDir,
      env: {
        ...process.env,
        FLASK_ENV: isDev ? 'development' : 'production',
        FLASK_RUN_PORT: FLASK_PORT.toString(),
        PYTHONUNBUFFERED: '1',
        PYTHONIOENCODING: 'utf-8',
        PYTHONLEGACYWINDOWSSTDIO: '0',
        PYTHONUTF8: '1',
        ELECTRON_RUN_AS_NODE: 'true' // Signal to Flask that we're in Electron
      },
      stdio: ['ignore', 'pipe', 'pipe']
    };
    
    // On Windows, we need to be careful with shell option
    // Use shell: false but ensure Python path is absolute
    if (process.platform === 'win32') {
      // If Python path contains spaces, we need to quote it
      // But spawn handles this better without shell
      spawnOptions.shell = false;
    }
    
    console.log('Spawning Flask with:', pythonExecutable, appPath);
    flaskProcess = spawn(pythonExecutable, [appPath], spawnOptions);

    flaskProcess.stdout.on('data', (data) => {
      console.log(`Flask: ${data}`);
    });

    flaskProcess.stderr.on('data', (data) => {
      console.error(`Flask Error: ${data}`);
      // Don't treat stderr as fatal - Flask logs to stderr
    });

    flaskProcess.on('error', (error) => {
      console.error('Failed to start Flask process:', error);
      dialog.showErrorBox(
        'Python Not Found',
        `Python is required to run the backend server.\n\n` +
        `Error: ${error.message}\n\n` +
        `Please install Python 3.11 or later and ensure it's in your PATH.\n` +
        `You can download Python from https://www.python.org/downloads/`
      );
      flaskProcess = null;
      app.quit();
    });

    flaskProcess.on('close', (code) => {
      console.log(`Flask process exited with code ${code}`);
      flaskProcess = null;
      
      if (code !== 0 && code !== null) {
        console.error('Flask server exited with error code:', code);
        // Don't quit immediately - give user a chance to see the error
        if (mainWindow) {
          dialog.showErrorBox(
            'Backend Server Error',
            `The backend server has stopped unexpectedly (exit code: ${code}).\n\n` +
            `Please check:\n` +
            `1. Python is installed and in PATH\n` +
            `2. Flask dependencies are installed (pip install -r requirements.txt)\n` +
            `3. Port ${FLASK_PORT} is not in use by another application\n\n` +
            `The application will close.`
          );
        }
        setTimeout(() => app.quit(), 2000);
      }
    });
  } catch (error) {
    console.error('Exception starting Flask:', error);
    dialog.showErrorBox(
      'Startup Error',
      `Failed to start backend server: ${error.message}`
    );
    app.quit();
  }
}

function createMenu() {
  const template = [
    {
      label: 'File',
      submenu: [
        { label: 'New File', accelerator: 'CmdOrCtrl+N', click: () => sendToRenderer('menu-new-file') },
        { label: 'Open File...', accelerator: 'CmdOrCtrl+O', click: () => sendToRenderer('menu-open-file') },
        { type: 'separator' },
        { label: 'Save', accelerator: 'CmdOrCtrl+S', click: () => sendToRenderer('menu-save') },
        { label: 'Save All', accelerator: 'CmdOrCtrl+Shift+S', click: () => sendToRenderer('menu-save-all') },
        { type: 'separator' },
        { label: 'Exit', accelerator: process.platform === 'darwin' ? 'Cmd+Q' : 'Ctrl+Q', click: () => app.quit() }
      ]
    },
    {
      label: 'Edit',
      submenu: [
        { label: 'Undo', accelerator: 'CmdOrCtrl+Z', role: 'undo' },
        { label: 'Redo', accelerator: 'CmdOrCtrl+Y', role: 'redo' },
        { type: 'separator' },
        { label: 'Cut', accelerator: 'CmdOrCtrl+X', role: 'cut' },
        { label: 'Copy', accelerator: 'CmdOrCtrl+C', role: 'copy' },
        { label: 'Paste', accelerator: 'CmdOrCtrl+V', role: 'paste' }
      ]
    },
    {
      label: 'View',
      submenu: [
        { label: 'Reload', accelerator: 'CmdOrCtrl+R', click: () => mainWindow.reload() },
        { label: 'Force Reload', accelerator: 'CmdOrCtrl+Shift+R', click: () => mainWindow.webContents.reloadIgnoringCache() },
        { label: 'Toggle Developer Tools', accelerator: 'F12', click: () => mainWindow.webContents.toggleDevTools() },
        { type: 'separator' },
        { label: 'Actual Size', accelerator: 'CmdOrCtrl+0', role: 'resetZoom' },
        { label: 'Zoom In', accelerator: 'CmdOrCtrl+Plus', role: 'zoomIn' },
        { label: 'Zoom Out', accelerator: 'CmdOrCtrl+-', role: 'zoomOut' },
        { type: 'separator' },
        { label: 'Toggle Fullscreen', accelerator: 'F11', role: 'togglefullscreen' }
      ]
    },
    {
      label: 'Help',
      submenu: [
        { label: 'About Auto_Punch IDE', click: () => showAboutDialog() },
        { label: 'Check for Updates', click: () => checkForUpdates() },
        { type: 'separator' },
        { label: 'Documentation', click: () => shell.openExternal('https://github.com/SMG-Dawn/Auto-Punch-IDE-Desktop') }
      ]
    }
  ];

  const menu = Menu.buildFromTemplate(template);
  Menu.setApplicationMenu(menu);
}

function sendToRenderer(channel, data) {
  if (mainWindow && mainWindow.webContents) {
    mainWindow.webContents.send(channel, data);
  }
}

function showAboutDialog() {
  dialog.showMessageBox(mainWindow, {
    type: 'info',
    title: 'About Auto_Punch IDE',
    message: 'Auto_Punch IDE',
    detail: `Version: ${app.getVersion()}\n\nProfessional IDE with AI assistance and RedTeam tools.\n\nPowered by Auto_Punch Ai`
  });
}

function checkForUpdates() {
  if (isDev) {
    dialog.showMessageBox(mainWindow, {
      type: 'info',
      title: 'Updates',
      message: 'Update checking is only available in the production version.'
    });
    return;
  }

  if (autoUpdater && autoUpdater.checkForUpdates) {
    try {
      autoUpdater.checkForUpdates();
      dialog.showMessageBox(mainWindow, {
        type: 'info',
        title: 'Checking for Updates',
        message: 'Checking for updates...'
      });
    } catch (error) {
      dialog.showMessageBox(mainWindow, {
        type: 'info',
        title: 'Updates',
        message: 'Update checking is not available in this version.'
      });
    }
  } else {
    dialog.showMessageBox(mainWindow, {
      type: 'info',
      title: 'Updates',
      message: 'Update checking is not available in this version.'
    });
  }
}

// App event handlers
app.whenReady().then(() => {
  startFlaskServer();
  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on('window-all-closed', () => {
  // On macOS, keep app running even when all windows are closed
  if (process.platform !== 'darwin') {
    // Stop Flask server
    if (flaskProcess) {
      flaskProcess.kill();
      flaskProcess = null;
    }
    app.quit();
  }
});

app.on('before-quit', () => {
  // Cleanup
  if (flaskProcess) {
    flaskProcess.kill();
    flaskProcess = null;
  }
});

// IPC handlers
ipcMain.handle('get-app-version', () => {
  return app.getVersion();
});

ipcMain.handle('get-app-path', () => {
  return app.getPath('userData');
});

// Handle certificate errors (for local development)
app.on('certificate-error', (event, webContents, url, error, certificate, callback) => {
  if (url.startsWith('http://localhost')) {
    event.preventDefault();
    callback(true);
  } else {
    callback(false);
  }
});

