import ssl
import os, platform
import urllib.request
import subprocess
from pathlib import Path

os = platform.system()
ssl._create_default_https_context = ssl._create_unverified_context

if (os == "Darwin"):
    pkgfile = ("GoogleChrome.pkg")
    arch = subprocess.getoutput('/usr/bin/uname -p')
    tmp = ('/tmp/')
    filePath = Path(tmp + pkgfile)
    if (arch == "i386") or (arch == "x86_64"):
        url = 'https://dl.google.com/chrome/mac/stable/gcem/GoogleChrome.pkg'
    elif (arch == "arm"):
        url = 'https://dl.google.com/dl/chrome/mac/universal/stable/gcem/GoogleChrome.pkg'
elif (os == "win32"):
    tmp = (C:\temp)
    url = ''
elif (os == 'win64'):
    tmp = (C:\temp)
    url = ''


with urllib.request.urlopen(url) as response, open(filePath, 'wb') as out_file:
    data = response.read()
    out_file.write(data)
