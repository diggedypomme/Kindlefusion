#!/bin/sh
#eips -c 

ip_output=$( ip addr show dev wlan0 | grep "inet " | awk '{print $2}')
echo "$ip_output"

#eips 10 10 "$ip_output"
/mnt/us/usbnet/bin/fbink -pmM -y -15 "$ip_output"

stringZ=abcABC123ABCabc
#       0123456789.....
#       0-based indexing.

echo ${stringZ:0}          # abcABC123ABCabc
echo ${stringZ:1}          # bcABC123ABCabc
echo ${stringZ:7}          # 23ABCabc

echo ${stringZ:7:3}        # 23A
                           # Three characters of substring.