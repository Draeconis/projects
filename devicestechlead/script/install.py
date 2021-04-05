import ssl, sys, os, platform, urllib.request, tempfile, subprocess
from pathlib import Path
from zipfile import ZipFile

os = platform.system()

# Turns Electron UI on or off. If 'False', we'll just install Chrome.
ui_enabled = True

# fix an issue downloading from an https share
ssl._create_default_https_context = ssl._create_unverified_context

# set $url based on os/arch
if (os == "Darwin"):
    electronApp = Path('/Users/geofsmi1/Documents/GitHub/Electron.app/Contents/MacOS/Electron')
    print("DEBUG: os is " + os)
    installer = "GoogleChrome.pkg"
    arch = subprocess.getoutput('/usr/bin/uname -p')
    print("DEBUG: arch is " + arch)
    if (arch == "i386") or (arch == "x86_64"):
        url = 'https://dl.google.com/chrome/mac/stable/gcem/GoogleChrome.pkg'
    elif (arch == "arm"):
        url = 'https://dl.google.com/dl/chrome/mac/universal/stable/gcem/GoogleChrome.pkg'
elif (os == "Windows"):
    electronApp = Path('C:/Users/geoff/Documents/electron/dist/electron.exe')
    print("DEBUG: os is " + os)
    installer = "GoogleChromeEnterpriseBundle.zip"
    is_64bits = sys.maxsize > 2**32
    print("DEBUG: is 64bit? " + str(is_64bits))
    if ( is_64bits == True ):
        url = 'https://dl.google.com/dl/chrome/install/GoogleChromeEnterpriseBundle64.zip'
    else:
        url = 'https://dl.google.com/dl/chrome/install/GoogleChromeEnterpriseBundle.zip'

# get the filesize of the file were about to download
# remoteFileSize = urllib.request.urlopen(url).length

# create a temp directory, removed once this script moves past the 'with' which creates it.
# on windows, this will be %appdata%\local\Temp\[random]\
# on macOS, this will be the DARWIN_USER_TEMP_DIR/[random]/
with tempfile.TemporaryDirectory() as directory:
    filePath = Path(directory + '/' + installer)
    # print("DEBUG: filePath is " + str(filePath))

    if (ui_enabled == True):
        # spawn Electron, open main page
        startAction = subprocess.run([electronApp, '--inpsect=5858', 'view=main'], capture_output=True, text=True).stdout.strip("\n")
        if (startAction != "start"):
            exit()

        downloadAction = subprocess.Popen([electronApp, 'view=download'])

        # spawn electron,open download page, download file and monitor progress
        # inputpath = "'inputpath=\"" + url + "\"'"
        # outputpath = "'outputpath=\"" + str(filePath) + "\"'"
        # size = "'size=" + str(remoteFileSize) + "'"
        # subprocess.Popen([electronApp, 'view=download', outputpath, size])
        # print(inputpath)
        # print(outputpath)
        # print(size)

    # download the file quietly to the temp dir
    with urllib.request.urlopen(url) as response, open(filePath, 'wb') as out_file:
        data = response.read()
        out_file.write(data)

    if (ui_enabled == True):
        downloadAction.terminate()
        installAction = subprocess.Popen([electronApp, 'view=install'])

    # perform the installation
    if (os == "Darwin"):
        
    elif (os == "Windows"):
        ZipFile(filePath).extractall(directory)
