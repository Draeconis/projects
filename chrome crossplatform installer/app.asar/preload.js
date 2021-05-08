// All of the Node.js APIs are available in the preload process.
// It has the same sandbox as a Chrome extension.
// "use strict";
// Object.defineProperty(exports, "__esModule", { value: true });
// const electron_1 = require("electron");
const { ipcRenderer } = require('electron');

// async function initialize() {
//     const dlfilesizecheck = setInterval(function(){
//         ipcRenderer.invoke('download-progress').then((value) => {
//             if ((value).length > 0) {
//                 document.getElementById("progressBar").innerHTML = '<div class="progress-bar" role="progressbar" style="width: ' + value + '%;" aria-valuenow="' + value + '" aria-valuemin="0" aria-valuemax="100">' + value + '%</div>'
//             } else {
//                 clearInterval(dlfilesizecheck)
//             }
//         });
//     }, 500 );
// }

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
//     if (('#progressBar').length > 0) {
//         ipcRenderer.invoke('download-progress');
//     }
});

// electron_1.contextBridge.exposeInMainWorld('electronDefaultApp', {
//     initialize
// });
