import ssl, sys, os, platform, urllib.request, tempfile, subprocess
from pathlib import Path
from zipfile import ZipFile

os = platform.system()

# fix an issue downloading from an https share
ssl._create_default_https_context = ssl._create_unverified_context

# set $url based on os/arch
if (os == "Darwin"):
    print("DEBUG: os is " + os)
    installer = "GoogleChrome.pkg"
    arch = subprocess.getoutput('/usr/bin/uname -p')
    print("DEBUG: arch is " + arch)
    if (arch == "i386") or (arch == "x86_64"):
        url = 'https://dl.google.com/chrome/mac/stable/gcem/GoogleChrome.pkg'
    elif (arch == "arm"):
        url = 'https://dl.google.com/dl/chrome/mac/universal/stable/gcem/GoogleChrome.pkg'
elif (os == "Windows"):
    print("DEBUG: os is " + os)
    installer = "GoogleChromeEnterpriseBundle.zip"
    is_64bits = sys.maxsize > 2**32
    print("DEBUG: is 64bit? " + str(is_64bits))
    if ( is_64bits == True ):
        url = 'https://dl.google.com/dl/chrome/install/GoogleChromeEnterpriseBundle64.zip'
    else:
        url = 'https://dl.google.com/dl/chrome/install/GoogleChromeEnterpriseBundle.zip'

# get the filesize of the file were about to download
remoteFileSize = print(urllib.request.urlopen(url).length)

# create a temp directory, removed once this script moves past the 'with' which creates it.
# on windows, this will be %appdata%\local\Temp\[random]\
# on macOS, this will be the DARWIN_USER_TEMP_DIR/[random]/
with tempfile.TemporaryDirectory() as directory:
    filePath = Path(directory + '/' + installer)
    print("DEBUG: filePath is " + str(filePath))

    # spawn electron, pass it args
     subprocess.call([Electron])

    # download the file to the temp dir
    with urllib.request.urlopen(url) as response, open(filePath, 'wb') as out_file:
        data = response.read()
        out_file.write(data)

    # Electron should change its view to say installing..

    # perform the installation
    if (os == "Darwin"):
        stuff
    elif (os == "Windows"):
        ZipFile(filePath).extractall(directory)
