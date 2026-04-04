const { contextBridge, ipcRenderer } = require("electron");

contextBridge.exposeInMainWorld("electronAPI", {
  getLicense: () => ipcRenderer.invoke("get-license"),
  getLicenseStatus: () => ipcRenderer.invoke("get-license-status"),
  activateLicense: (key) => ipcRenderer.invoke("activate-license", key),
  getSettings: () => ipcRenderer.invoke("get-settings"),
  saveSettings: (settings) => ipcRenderer.invoke("save-settings", settings),
  selectFile: () => ipcRenderer.invoke("select-file"),
  isDesktop: true,
});
