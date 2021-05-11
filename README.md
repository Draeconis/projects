acd_brightness is a couple of projects to script control of the LED Cinema Display (27-inch).
first attempt was editing reg settings, which while the script works, does nothing to solve the problem :)
second attempt fires USB control transfer commands straight at the display, which alarmingly, works!



chrome crossplatform installer is a more expansive project, investigating creating a basic install script for chrome, but that needs to run on windows or macOS seamlessly
this also uses Electron as a UI, but is very basic.
prerequisite scripts for macos and windows are also present, allowing clients to ensure python3 is installed
macos big sur changes this up a bit, so be careful



roller is an earlier script, part an interesting challenge series. written in bash, hastily googled.
