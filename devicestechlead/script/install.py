import ssl
import sys
import os, platform
import urllib.request
import subprocess
from pathlib import Path

os = platform.system()
ssl._create_default_https_context = ssl._create_unverified_context

if (os == "Darwin"):
    installer = "GoogleChrome.pkg"
    arch = subprocess.getoutput('/usr/bin/uname -p')
    tmp = ('/tmp/')
    if (arch == "i386") or (arch == "x86_64"):
        url = 'https://dl.google.com/chrome/mac/stable/gcem/GoogleChrome.pkg'
    elif (arch == "arm"):
        url = 'https://dl.google.com/dl/chrome/mac/universal/stable/gcem/GoogleChrome.pkg'
elif (os == "Windows"):
    installer = "GoogleChromeEnterpriseBundle.zip"
    is_64bits = sys.maxsize > 2**32
    tmp = ('C:/temp/')
    if ( is_64bits == True ):
        url = 'https://dl.google.com/dl/chrome/install/GoogleChromeEnterpriseBundle64.zip'
    else:
        url = 'https://dl.google.com/dl/chrome/install/GoogleChromeEnterpriseBundle.zip'

filePath = Path(tmp + installer)
with urllib.request.urlopen(url) as response, open(installer, 'wb') as out_file:
    data = response.read()
    out_file.write(data)
