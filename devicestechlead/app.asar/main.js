// Modules to control application life and create native browser window
const {app, BrowserWindow} = require('electron')
const path = require('path')
const { ipcMain } = require('electron');
var nodeConsole = require('console');
var outputConsole = new nodeConsole.Console(process.stdout, process.stderr);
import fs from 'fs';

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
} else {
  app.quit()
}

  // Open the DevTools.
  // mainWindow.webContents.openDevTools()
}

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

ipcMain.handle('download-progress', () => {
  const sourceUrl = global.passedargs['inputpath'];
  const targetFile = global.passedargs['outputpath'];
  const length = global.passedargs['size'];
  export default async function download(sourceUrl, targetFile, progressCallback, length) {
  const request = new Request(sourceUrl, {
    headers: new Headers({'Content-Type': 'application/octet-stream'})
  });

  const response = await fetch(request);
  if (!response.ok) {
    throw Error(`Unable to download, server returned ${response.status} ${response.statusText}`);
  }

  const body = response.body;
  if (body == null) {
    throw Error('No response body');
  }

  const finalLength = length || parseInt(response.headers.get('Content-Length' || '0'), 10);
  const reader = body.getReader();
  const writer = fs.createWriteStream(targetFile);

  await streamWithProgress(finalLength, reader, writer, progressCallback);
  writer.end();
}

async function streamWithProgress(length, reader, writer, progressCallback) {
  let bytesDone = 0;

  while (true) {
    const result = await reader.read();
    if (result.done) {
      if (progressCallback != null) {
        progressCallback(length, 100);
      }
      return;
    }

    const chunk = result.value;
    if (chunk == null) {
      throw Error('Empty chunk received during download');
    } else {
      writer.write(Buffer.from(chunk));
      if (progressCallback != null) {
        bytesDone += chunk.byteLength;
        const percent = length === 0 ? null : Math.floor(bytesDone / length * 100);
        progressCallback(bytesDone, percent);
      }
    }
  }
}
});


// ipcMain.handle('watch-progress', () => {
    // const dlfile = (global.passedargs['path']);
    // const fileMax = (global.passedargs['size']);
    // outputConsole.log(fileMax);
    // return fileMax;

    // if (dlfile.length > 0) {
    //   const dlfilesizecheck = setInterval(function(){
    //     const dlfilesize =
    //     if (dlfilesize != fileMax) {
    //       percentage = Math.ceil(dlfilesize / fileMax * 100)
    //       return percentage;
    //     } else {
    //       clearInterval(dlfilesizecheck);
    //     }
    //       stuff
    //     }
    //   }, 500 );
    // }
// });
