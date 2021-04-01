import ssl
import sys
import os, platform
import urllib.request
import tempfile
import subprocess
from pathlib import Path

os = platform.system()
ssl._create_default_https_context = ssl._create_unverified_context

if (os == "Darwin"):
    print("DEBUG: os is " + os)
    installer = "GoogleChrome.pkg"
    arch = subprocess.getoutput('/usr/bin/uname -p')
    print("DEBUG: arch is " + arch)
    tmp = ('/tmp/')
    if (arch == "i386") or (arch == "x86_64"):
        url = 'https://dl.google.com/chrome/mac/stable/gcem/GoogleChrome.pkg'
    elif (arch == "arm"):
        url = 'https://dl.google.com/dl/chrome/mac/universal/stable/gcem/GoogleChrome.pkg'
elif (os == "Windows"):
    print("DEBUG: os is " + os)
    installer = "GoogleChromeEnterpriseBundle.zip"
    is_64bits = sys.maxsize > 2**32
    tmp = ('C:/temp/')
    print("DEBUG: is 64bit? " + str(is_64bits))
    if ( is_64bits == True ):
        url = 'https://dl.google.com/dl/chrome/install/GoogleChromeEnterpriseBundle64.zip'
    else:
        url = 'https://dl.google.com/dl/chrome/install/GoogleChromeEnterpriseBundle.zip'

# if Path(tmp).is_dir():
#     filePath = Path(tmp + installer)
# else:


print("DEBUG: filePath is " + str(filePath))

with urllib.request.urlopen(url) as response, open(filePath, 'wb') as out_file:
    data = response.read()
    out_file.write(data)
