const { contextBridge, ipcRenderer } = require('electron');

// Expose protected methods that allow the renderer process to use
// the ipcRenderer without exposing the entire object
contextBridge.exposeInMainWorld('electronAPI', {
  getVersion: () => ipcRenderer.invoke('get-app-version'),
  getAppPath: () => ipcRenderer.invoke('get-app-path'),
  onMenuAction: (callback) => {
    ipcRenderer.on('menu-new-file', callback);
    ipcRenderer.on('menu-open-file', callback);
    ipcRenderer.on('menu-save', callback);
    ipcRenderer.on('menu-save-all', callback);
  }
});


