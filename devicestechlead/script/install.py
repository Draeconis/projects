import ssl, sys, os, platform, urllib.request, tempfile, subprocess, logging
from pathlib import Path
from zipfile import ZipFile
from time import sleep
from socket import gethostname

clientos = platform.system()
hostname = gethostname()

scriptName = "GoogleChromeInstaller"
scriptVersion = "1.3"
arch = ""
is_64bits = ""

# Turns Electron UI on or off. If 'False', we'll just install Chrome.
ui_enabled = True

# fix an issue downloading from an https share
ssl._create_default_https_context = ssl._create_unverified_context

# set $url based on os/arch
if (clientos == "Darwin"):
    currentDir = Path(__file__).parent.absolute()
    electronApp = Path(str(currentDir) + '/Electron')
    installer = Path('/usr/sbin/installer')
    download = "GoogleChrome.pkg"
    arch = subprocess.getoutput('/usr/bin/uname -p')
    logfile = Path('/var/log/company.log')
    if (arch == "i386") or (arch == "x86_64"):
        url = 'https://dl.google.com/chrome/mac/stable/gcem/GoogleChrome.pkg'
    elif (arch == "arm"):
        url = 'https://dl.google.com/dl/chrome/mac/universal/stable/gcem/GoogleChrome.pkg'
elif (clientos == "Windows"):
    electronApp = Path('electron.exe')
    msiexec = Path('C:/Windows/System32/msiexec.exe')
    download = "GoogleChromeEnterpriseBundle.zip"
    logfile = Path('C:/Windows/System32/winevt/Logs/company.log')
    is_64bits = sys.maxsize > 2**32
    print("DEBUG: is 64bit? " + str(is_64bits))
    if ( is_64bits == True ):
        url = 'https://dl.google.com/dl/chrome/install/GoogleChromeEnterpriseBundle64.zip'
    else:
        url = 'https://dl.google.com/dl/chrome/install/GoogleChromeEnterpriseBundle.zip'

logging.basicConfig(filename=logfile, format='%(asctime)s ' + hostname + " " + scriptName + "-" + scriptVersion + ' %(levelname)s: %(message)s', datefmt='%a %b %d %H:%M:%S', encoding='utf-8', level=logging.DEBUG)

def log(level, msg):
    print(scriptName + ": " + level + ": " + msg)
    if (level == "debug"):
        logging.debug(msg)
    elif (level == "info"):
        logging.info(msg)
    elif (level == "warning"):
        logging.warning(msg)
    elif (level == "error"):
        logging.error(msg)
    elif (level == "critical"):
        logging.critical(msg)

log('info', '*** log start')
log('info', 'clientos is ' + clientos)
if (arch != ""):
    log('info', 'arch is ' + arch)
if (is_64bits != ""):
    log('info', 'clientos is 64bit: ' + str(is_64bits))

log('debug', 'url is ' + url)

# get the filesize of the file were about to download
# remoteFileSize = urllib.request.urlopen(url).length

# create a temp directory, removed once this script moves past the 'with' which creates it.
# on windows, this will be %appdata%\local\Temp\[random]\
# on macOS, this will be the DARWIN_USER_TEMP_DIR/[random]/.. or sometimes /tmp/[random]/
with tempfile.TemporaryDirectory() as directory:
    filePath = Path(directory + '/' + download)
    log('debug', 'filePath is ' + str(filePath))

    if (ui_enabled == True):
        # spawn Electron, open main page
        log('info', 'launching electron, startAction')
        startAction = subprocess.run([electronApp, 'view=main'], capture_output=True, text=True).stdout.strip("\n")
        if (startAction != "start"):
            exit()

        log('debug', 'startAction result was ' + startAction)
        log('info', 'launching electron, downloadAction')
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
    log('info', 'starting file download')
    with urllib.request.urlopen(url) as response, open(filePath, 'wb') as out_file:
        data = response.read()
        out_file.write(data)

    # close and reopen electron back up if UI is enabled, letting the user know the installer is now installing
    if (ui_enabled == True):
        downloadAction.terminate()
        log('info', 'killing downloadAction, starting installAction')
        installAction = subprocess.Popen([electronApp, 'view=install'])

    # perform the installation
    log('info', 'installing Chrome')
    if (clientos == "Darwin"):
        log('debug', 'installing ' + str(filePath))
        subprocess.run([installer, '-pkg', filePath, '-target', '/'])
    elif (clientos == "Windows"):
        log('debug', 'unzipping ' + str(filePath) + ' to ' + str(directory))
        ZipFile(filePath).extractall(directory)
        installPath = Path(str(directory) + '/Installers')
        if ( is_64bits == True ):
            installMSI = Path(str(installPath) + '/GoogleChromeStandaloneEnterprise64.msi')
        else:
            installMSI = Path(str(installPath) + '/GoogleChromeStandaloneEnterprise.msi')
        log('debug', 'installing ' + str(installMSI))
        subprocess.run([msiexec, '/i', installMSI, '/qn', '/norestart'])

    # electron prompt that install is complete
    if (ui_enabled == True):
        installAction.terminate()
        log('info', 'killing installAction, starting postInstallAction')
        postInstallAction = subprocess.Popen([electronApp, 'view=postinstall'])
        sleep(10)
        postInstallAction.terminate()
        log('info', 'done!')
exit()
