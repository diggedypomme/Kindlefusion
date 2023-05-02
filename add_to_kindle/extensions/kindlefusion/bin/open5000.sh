# python3 -m ensurepip --upgrade
#/mnt/us/python3/bin/pip3 install flask
iptables -A INPUT -p tcp --dport 5000 -i wlan0 -j ACCEPT
echo "opened"
mntroot rw
echo "writeable"
#eips -c
#eips 10 10 "port opened and made writeable"
/mnt/us/usbnet/bin/fbink -pmM -y -6 "port opened and made writeable"
