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
    ipcRenderer.invoke('download-progress');
    });
  };
});


// if (('#progressBar').length > 0) {
//   ipcRenderer.invoke('watch-progress').then((value) => {
//     document.getElementById("progressBar").
//     console.log(value);
//   });
// };
