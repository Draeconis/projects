#!/bin/bash

url="https://www.python.org/ftp/python/3.9.2/python-3.9.2-macos11.pkg"
pkgfile="python.pkg"

/usr/bin/curl -L -s ${url} -o /tmp/${pkgfile}
if [[ ! -e /tmp/${pkgfile} ]]; then
	echo "error, download failed. exiting."
	exit 1
fi
echo "Installing.."
/usr/sbin/installer -pkg /tmp/${pkgfile} -target / >/dev/null 2>&1
/bin/sleep 10
echo "Deleting $pkgfile"
/bin/rm /tmp/"${pkgfile}"

exit 0
