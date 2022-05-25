#!/bin/bash

# The IP for the server you wish to ping (8.8.8.8 is a public Google DNS server)
SERVER=192.168.1.1

# Only send two pings, sending output to /dev/null
ping -c4 ${SERVER} > /dev/null

# If the return code from ping ($?) is not 0 (meaning there was an error)
if [ $? != 0 ]
then
   	date >> /var/log/wifi_reboot.log
	echo "Rebooting wifi" >> /var/log/wifi_reboot.log
	# Restart the wireless interface
	ifconfig wlan0 down
	sleep 5
	ifconfig wlan0 up
	if [ $? != 0 ]
	then
		echo "Error Rebooting" >> /var/log/wifi_reboot.log
	fi
fi
