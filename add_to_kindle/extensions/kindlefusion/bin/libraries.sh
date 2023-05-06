#!/bin/sh

eips -c

touch "/mnt/us/documents/My Clippings.txt"

mntroot rw

eips -c

eips 14 5 "Installing libraries"

eips 10 12 "Installing PIP"
python3 -m ensurepip --upgrade
eips 39 12 "Done"

eips 10 14 "Installing Flask"
/mnt/us/python3/bin/pip3 install flask
eips 39 14 "Done"

eips 10 16 "Installing Loguru"
/mnt/us/python3/bin/pip3 install loguru
eips 39 16 "Done"

eips 10 18 "Installing Flask_cors"
/mnt/us/python3/bin/pip3 install flask_cors
eips 39 18 "Done"

eips 24 27 "Done"
eips 14 29 "Press up to continue"
