$is_64bit = [Environment]::Is64BitOperatingSystem
$exeFile = "python.exe"
$exeFilePath = "$env:appdata\$exeFile"

if($is_64bit -eq $true) {
  $url = ("https://www.python.org/ftp/python/3.9.2/python-3.9.2-amd64.exe")
} else {
  $url = ("https://www.python.org/ftp/python/3.9.2/python-3.9.2.exe")
}

Invoke-WebRequest -Uri $url -OutFile $exeFilePath
if (!(Test-Path $exeFilePath)) {
  Write-Host "error, download failed. exiting."
  exit
}
Write-Host "Installing.."
# https://docs.python.org/3.9/using/windows.html
start-process -filepath $exeFilePath -argumentlist '/quiet', 'InstallAllUsers=1', 'PrependPath=1', 'Include_test=0', 'SimpleInstall=1'
Start-Sleep -s 10
Write-Host "Deleting $exeFile"
Remove-Item $exeFilePath

exit
