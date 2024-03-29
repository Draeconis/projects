// Modules to control application life and create native browser window
const {app, BrowserWindow} = require('electron')
const path = require('path')
const { ipcMain } = require('electron');
var nodeConsole = require('console');
var outputConsole = new nodeConsole.Console(process.stdout, process.stderr);
const fs = require("fs");
// const ProgressBar = require('electron-progressbar');

const argv = process.argv.slice(1);
function createWindow () {
  // Create the browser window.
  const mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    frame: true,
    resizable: false,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      sandbox: true,
      enableRemoteModule: false,
      nodeIntegration: true
    },
    useContentSize: true,
  })

global.passedargs = {}
var slicedArgs = Array.prototype.slice.call(process.argv, 1).forEach(function(item) {items = item.split("="); global.passedargs[items[0]] = items[1] })

if (global.passedargs['view'] == "main"){
    mainWindow.loadFile('index.html')
} else if (global.passedargs['view'] == "download"){
    mainWindow.loadFile('download.html')
} else if (global.passedargs['view'] == "install"){
    mainWindow.loadFile('install.html')
} else if (global.passedargs['view'] == "postinstall"){
    mainWindow.loadFile('postinstall.html')
} else {
  app.quit()
}


  // Open the DevTools.
  // mainWindow.webContents.openDevTools()
}

// const targetFile = global.passedargs['outputpath'];
// var length = global.passedargs['size'];

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.whenReady().then(() => {
  createWindow()

  app.on('activate', function () {
    // On macOS it's common to re-create a window in the app when the
    // dock icon is clicked and there are no other windows open.
    if (BrowserWindow.getAllWindows().length === 0) createWindow()
  })
})

// Quit when all windows are closed, except on macOS. There, it's common
// for applications and their menu bar to stay active until the user quits
// explicitly with Cmd + Q.
app.on('window-all-closed', function () {
  if (process.platform !== 'darwin') app.quit()
})

// In this file you can include the rest of your app's specific main process
// code. You can also put them in separate files and require them here.

ipcMain.handle('quit-app', () => {
    process.exit(0);
});

ipcMain.handle('start', () => {
    outputConsole.log('start');
    process.exit(0);
});

// ipcMain.handle('download-progress', () => {
//     // const sourceUrl = global.passedargs['inputpath'];
//     const targetFile = global.passedargs['outputpath'];
//     var length = global.passedargs['size'];
//
//     fs.stat(targetFile, (err, fileStats) => {
//         if (err) {
//             console.log(err)
//         } else {
//             var currentSize = fileStats.size
//             if (currentSize != length) {
//                 var percentage = Math.ceil(currentSize / length * 100)
//                 // outputConsole.log('exit for some reason');
//                 return percentage;
//             } else {
//                 outputConsole.log('exit for some reason');
//                 // process.exit(0);
//             }
//         }
//     })
// });
