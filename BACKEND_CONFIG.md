# 🔧 Backend Configuration

## 📋 How the Backend Works

The Auto_Punch IDE desktop app uses a **Flask (Python) backend** that runs locally.

### Architecture

1. **Electron App** (Frontend)
   - Opens a browser window
   - Connects to Flask server on `http://localhost:5001`

2. **Flask Server** (Backend)
   - Runs Python `app.py`
   - Serves the web interface
   - Handles API requests
   - Manages WebSocket connections

## ⚠️ Current Issue

**Error:** "Backend server stopped unexpectedly"

### Why This Happens

1. **Python Not Found**
   - Python isn't installed
   - Python isn't in PATH
   - Wrong Python version

2. **Flask Dependencies Missing**
   - `requirements.txt` not installed
   - Missing Flask, Flask-SocketIO, etc.

3. **File Path Issues**
   - `app.py` not found in packaged app
   - Working directory incorrect

4. **Port Already in Use**
   - Port 5001 is used by another app
   - Previous Flask instance still running

## ✅ Requirements

### For the App to Work:

1. **Python 3.11+ Installed**
   - Download from: https://www.python.org/downloads/
   - Check: `python --version` in command prompt
   - Must be in PATH

2. **Flask Dependencies Installed**
   ```bash
   pip install -r requirements.txt
   ```

3. **Port 5001 Available**
   - Not used by another application
   - Firewall allows localhost connections

## 🔧 Fixes Applied

### 1. Better Error Handling
- Shows specific error messages
- Checks for Python before starting
- Validates file paths

### 2. Python Detection
- Tries multiple Python paths
- Checks common installation locations
- Uses shell to find Python in PATH

### 3. Path Resolution
- Tries multiple locations for `app.py`
- Validates file exists before starting
- Better working directory handling

### 4. User-Friendly Messages
- Clear error messages
- Installation instructions
- Troubleshooting tips

## 🚀 How to Fix

### Step 1: Install Python
```powershell
# Check if Python is installed
python --version

# If not installed, download from:
# https://www.python.org/downloads/
```

### Step 2: Install Dependencies
```powershell
cd "C:\Users\Administrator\Auto_Punch IDE"
pip install -r requirements.txt
```

### Step 3: Test Flask Manually
```powershell
python app.py
```

Should see:
```
 * Running on http://127.0.0.1:5001
```

### Step 4: Rebuild Installer
```powershell
.\fix-and-rebuild.ps1
```

## 📝 Notes

- **Python is Required:** The app needs Python to run the backend
- **Not Bundled:** Python isn't included in the installer (would be too large)
- **System Python:** Uses the system Python installation
- **Port 5001:** Must be available for the app to work

## 🔍 Troubleshooting

### Check Python:
```powershell
python --version
where python
```

### Check Flask:
```powershell
pip list | findstr flask
```

### Check Port:
```powershell
netstat -ano | findstr :5001
```

### Manual Test:
```powershell
python app.py
# Should start Flask server
# Open http://localhost:5001 in browser
```

## ✅ Summary

The backend requires:
1. ✅ Python 3.11+ installed
2. ✅ Flask dependencies installed
3. ✅ Port 5001 available
4. ✅ app.py accessible

The Electron app will now show better error messages if any of these are missing!


