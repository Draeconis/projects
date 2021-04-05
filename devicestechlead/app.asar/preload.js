// All of the Node.js APIs are available in the preload process.
// It has the same sandbox as a Chrome extension.
const { ipcRenderer } = require('electron');

window.addEventListener('DOMContentLoaded', () => {
    async function initialize() {
        const dlfilesizecheck = setInterval(function(){
            ipcRenderer.invoke('download-progress').then((value) => {
                if ((value).length > 0) {
                    document.getElementById("progressBar").innerHTML = '<div class="progress-bar" role="progressbar" style="width: ' + value + '%;" aria-valuenow="' + value + '" aria-valuemin="0" aria-valuemax="100">' + value + '%</div>'
                } else {
                    clearInterval(dlfilesizecheck)
                }
            });
        }, 500 );
    }
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
        initialize
    }
});



// initialize

// function createFileDLCheckLoop() {
//     const deferTimer = setInterval(function(){
//         if ( ttl > 1 ) {
//             ttl = ttl - 1;
//             document.getElementById("globalTimer").innerHTML = (ttl);
//             if ( ttl == 1 ) {
//                 document.getElementById("mins").innerHTML = ("minute");
//             }
//         } else {
//             outputConsole.log("1 Hour");
//             clearInterval(deferTimer);
//             var window = remote.getCurrentWindow();
//             ipcRenderer.send('quit-app');
//         }
//     }, 60000 );
// }
