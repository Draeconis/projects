// All of the Node.js APIs are available in the preload process.
// It has the same sandbox as a Chrome extension.
const { ipcRenderer } = require('electron');

window.addEventListener('DOMContentLoaded', () => {
  if (('#exitBtn').length > 0) {
    document.getElementById("exitBtn").addEventListener("click", (e) => {
        ipcRenderer.invoke('quit-app');
    });
  };
  if (('#startBtn').length > 0) {
    document.getElementById("startBtn").addEventListener("click", (e) => {
        ipcRenderer.invoke('start');
    });
  };
  if (('#progressBar').length > 0) {
    async function initialize() {
      ipcRenderer.invoke('read-flag').then((value) => {
        document.getElementById("progressBar").stuff(value)
      });
    }
  }
});
