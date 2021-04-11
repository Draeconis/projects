import winreg

# open HKEY_USERS reg entry
HKEY_USERS = winreg.ConnectRegistry(None,winreg.HKEY_USERS)
keyVal = r'S-1-5-21-2097320953-2311482321-2132067069-1001\Software\Apple Inc.\Brightness'

try:
    # jump to the subkey we're interested in. 'reserved' os always 0, access being '983103' is dec for '0xF003F', hex key for 'KEY_ALL_ACCESS''
    key = winreg.OpenKey(HKEY_USERS, keyVal, reserved=0, access=983103)
except:
    # subkey was missing, create it instead
    key = winreg.CreateKey(HKEY_USERS, keyVal)

# lastExternalBrightness is a REG_DWORD, and winreg.REG_DWORD is 4
winreg.SetValueEx(key, 'lastExternalBrightness', 0, 4, 25)
winreg.FlushKey(key)
winreg.CloseKey(key)
