import os, platform
import urllib.request
import subprocess
from pathlib import Path

os = platform.system()

if (os == "Darwin"):
    pkgfile = ("GoogleChrome.pkg")
    arch = subprocess.getoutput('/usr/bin/uname -p')
    tmp = ('/tmp/')
    filePath = (tmp + pkgfile)
    if (arch == "i386"):
        url = 'https://dl.google.com/chrome/mac/stable/gcem/GoogleChrome.pkg'
    elif (arch == "x86_64"):
        url = 'https://dl.google.com/chrome/mac/stable/gcem/GoogleChrome.pkg'
    elif (arch == "arm"):
        url = 'https://dl.google.com/dl/chrome/mac/universal/stable/gcem/GoogleChrome.pkg'
elif (os == "win32"):
    tmp = (C:\temp)
    url = ''
elif (os == 'win64'):
    tmp = (C:\temp)
    url = ''


urllib.request.urlretrieve(url, filePath)
